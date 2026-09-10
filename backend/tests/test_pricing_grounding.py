import asyncio
from types import SimpleNamespace

from app.services import chat_service as chat_service_module
from app.services.grounding import remove_unverified_currency_amounts


def test_no_source_prompt_forbids_unverified_exact_prices(monkeypatch):
    captured_messages = []

    monkeypatch.setattr(chat_service_module, "retrieve", lambda message, n_results=1: [])
    monkeypatch.setattr(chat_service_module.memory_service, "load_recent", lambda conversation_id, limit=3: [])
    monkeypatch.setattr(chat_service_module.memory_service, "save_message", lambda *args: None)

    class FakeLLM:
        async def ainvoke(self, messages):
            captured_messages.extend(messages)
            return SimpleNamespace(content="Price not verified. Please check the operator for current fares.")

    monkeypatch.setattr(chat_service_module, "llm", FakeLLM())

    response = asyncio.run(chat_service_module.chat_service.chat("What is the real taxi fare?", 1))
    prompt = "\n".join(str(message.content) for message in captured_messages)

    assert response.startswith("Price not verified")
    assert "Never invent" in prompt
    assert "No verified travel sources were retrieved" in prompt
    assert "250" not in prompt


def test_unverified_currency_amounts_are_removed():
    answer = "The fare is around INR 2000-3000, but check locally."

    sanitized = remove_unverified_currency_amounts(answer, has_verified_context=False)

    assert "2000" not in sanitized
    assert "3000" not in sanitized
    assert "price not verified" in sanitized