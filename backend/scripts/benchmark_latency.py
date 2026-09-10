"""Measure live WonderWise API latency.

Run from the backend directory while the API and Ollama are running:
    python scripts/benchmark_latency.py
"""

import json
import sys
import time
import urllib.error
import urllib.request
import uuid

try:
    import websocket
except ImportError:
    websocket = None

BASE_URL = "http://127.0.0.1:8000"
WS_URL = "ws://127.0.0.1:8000/ws/chat"


def request(path: str, method: str = "GET", body: dict | None = None, token: str | None = None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    payload = json.dumps(body).encode() if body is not None else None
    request_object = urllib.request.Request(
        BASE_URL + path,
        data=payload,
        headers=headers,
        method=method,
    )
    with urllib.request.urlopen(request_object, timeout=120) as response:
        return response.status, json.loads(response.read())


def elapsed_ms(callback):
    started = time.perf_counter()
    result = callback()
    return result, (time.perf_counter() - started) * 1000


def main():
    health_result, health_ms = elapsed_ms(lambda: request("/health"))
    assert health_result[0] == 200
    email = f"benchmark-{uuid.uuid4().hex}@example.com"
    auth_result, auth_ms = elapsed_ms(
        lambda: request(
            "/auth/register",
            "POST",
            {"email": email, "password": "strong-pass-123"},
        )
    )
    assert auth_result[0] == 201
    _, auth = request(
        "/auth/login",
        "POST",
        {"email": email, "password": "strong-pass-123"},
    )
    token = auth["access_token"]
    conversation_result, conversation_ms = elapsed_ms(
        lambda: request(
            "/conversations",
            "POST",
            {"title": "Latency benchmark"},
            token,
        )
    )
    assert conversation_result[0] == 201
    _, conversation = request(
        "/conversations",
        "POST",
        {"title": "Latency benchmark 2"},
        token,
    )
    conversation_id = conversation["id"]

    query = "Give one concise travel tip for Jaipur."
    chat_result, http_chat_ms = elapsed_ms(
        lambda: request(
            "/chat",
            "POST",
            {"message": query, "conversation_id": conversation_id},
            token,
        )
    )

    print("WonderWise latency benchmark")
    print(f"health_ms={health_ms:.1f}")
    print(f"auth_register_ms={auth_ms:.1f}")
    print(f"conversation_create_ms={conversation_ms:.1f}")
    print(f"http_chat_total_ms={http_chat_ms:.1f}")
    print(f"http_response_chars={len(chat_result[1]['response'])}")

    if websocket is None:
        print("websocket_benchmark=skipped (websocket-client is not installed)")
        return

    socket = websocket.create_connection(
        f"{WS_URL}?token={token}",
        timeout=120,
    )
    started = time.perf_counter()
    socket.send(json.dumps({
        "message": query,
        "conversation_id": conversation_id,
        "request_id": "latency-benchmark",
    }))
    first_message = json.loads(socket.recv())
    first_token_ms = (time.perf_counter() - started) * 1000
    chunks = 1
    while True:
        message = json.loads(socket.recv())
        if message["type"] == "end":
            break
        chunks += 1
    websocket_total_ms = (time.perf_counter() - started) * 1000
    socket.close()
    print(f"websocket_first_message_ms={first_token_ms:.1f}")
    print(f"websocket_total_ms={websocket_total_ms:.1f}")
    print(f"websocket_messages={chunks}")


if __name__ == "__main__":
    try:
        main()
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        print(f"Benchmark failed: {error}", file=sys.stderr)
        raise SystemExit(1)
