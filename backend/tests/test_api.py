from fastapi.testclient import TestClient
from uuid import uuid4

from app.services import chat_service as chat_service_module
from main import app


client = TestClient(app)


def register_user() -> tuple[dict, dict]:
    email = f"phase2-{uuid4().hex}@example.com"
    response = client.post("/auth/register", json={"email": email, "password": "strong-pass-123"})
    assert response.status_code == 201
    return response.json(), {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_unauthenticated_chat_is_rejected():
    response = client.post("/chat", json={"message": "hello", "conversation_id": 1})

    assert response.status_code == 401


def test_chat_rejects_blank_message():
    _, headers = register_user()
    response = client.post("/chat", headers=headers, json={"message": "   "})

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"


def test_chat_rejects_invalid_conversation_id():
    _, headers = register_user()
    response = client.post("/chat", headers=headers, json={"message": "Hello", "conversation_id": 0})

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"


def test_chat_returns_request_id_and_response(monkeypatch):
    _, headers = register_user()
    conversation = client.post("/conversations", headers=headers, json={"title": "Test trip"})
    expected_conversation_id = conversation.json()["id"]

    async def fake_chat(message: str, conversation_id: int):
        assert message == "Plan a short trip"
        assert conversation_id == expected_conversation_id
        return "Test itinerary"

    monkeypatch.setattr(chat_service_module.chat_service, "chat", fake_chat)

    response = client.post(
        "/chat",
        headers={**headers, "X-Request-ID": "test-request-1"},
        json={"message": "  Plan a short trip  ", "conversation_id": expected_conversation_id},
    )

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == "test-request-1"
    assert response.json()["response"] == "Test itinerary"
    assert response.json()["structured"]["answer"] == "Test itinerary"


def test_conversation_is_private_to_its_owner():
    _, owner_headers = register_user()
    _, other_headers = register_user()
    response = client.post("/conversations", headers=owner_headers, json={"title": "Private trip"})
    conversation_id = response.json()["id"]

    forbidden = client.patch(
        f"/conversations/{conversation_id}",
        headers=other_headers,
        json={"title": "Hijacked"},
    )

    assert forbidden.status_code == 404