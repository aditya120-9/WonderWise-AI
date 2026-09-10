import asyncio
import time

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from app.llm.ollama_client import llm
from app.prompts.system_prompt import SYSTEM_PROMPT
from app.rag.retriever import retrieve
from app.memory.memory_service import memory_service
from app.services.response_parser import append_source_citations
from app.services.grounding import remove_unverified_currency_amounts
from app.config.settings import settings
from app.observability.metrics import metrics


class ChatService:

    async def chat(self, message: str, conversation_id: int = 1):
        if message.strip().lower() in {"hi", "hello", "hey", "hey there"}:
            response = "Hi! I'm WonderWise AI. Where would you like to travel?"
            await asyncio.gather(
                asyncio.to_thread(memory_service.save_message, conversation_id, "user", message),
                asyncio.to_thread(memory_service.save_message, conversation_id, "assistant", response),
            )
            return response

        # Keep the prompt lightweight for fast local inference without losing relevant context.
        retrieved, history_items = await asyncio.gather(
            asyncio.to_thread(retrieve, message, n_results=4),
            asyncio.to_thread(memory_service.load_recent, conversation_id, limit=3),
        )

        context_text = ""
        if retrieved:
            blocks = []
            for item in retrieved:
                source = item["metadata"].get("source", "unknown")
                doc = item.get("document", "")
                doc = doc[:2200]
                blocks.append(f"Source: {source}\n{doc}")

            context_text = "\n\n".join(blocks)[:8000]

        prompt_messages = [SystemMessage(content=SYSTEM_PROMPT)]
        if context_text:
            prompt_messages.append(HumanMessage(content=f"Context:\n{context_text}"))
        else:
            prompt_messages.append(
                HumanMessage(
                    content=(
                        "No verified travel sources were retrieved for this request. "
                        "Do not state numeric prices or availability; say price not verified."
                    )
                )
            )

        for item in reversed(history_items):
            if item.role == "assistant":
                prompt_messages.append(AIMessage(content=item.content))
            else:
                prompt_messages.append(HumanMessage(content=item.content))

        prompt_messages.append(HumanMessage(content=message))
        await asyncio.to_thread(memory_service.save_message, conversation_id, "user", message)

        llm_started_at = time.perf_counter()
        try:
            response = await asyncio.wait_for(
                llm.ainvoke(prompt_messages),
                timeout=settings.LLM_TIMEOUT_SECONDS,
            )
        except asyncio.TimeoutError:
            metrics.increment("llm_timeouts")
            raise TimeoutError("The AI model took too long to respond")
        metrics.increment("llm_requests")
        metrics.observe("llm_duration_ms", (time.perf_counter() - llm_started_at) * 1000)
        response_text = remove_unverified_currency_amounts(
            append_source_citations(str(response.content), retrieved),
            has_verified_context=bool(retrieved),
        )
        await asyncio.to_thread(memory_service.save_message, conversation_id, "assistant", response_text)

        return response_text


chat_service = ChatService()

