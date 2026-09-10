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


class StreamService:

    async def stream(self, message: str, conversation_id: int = 1):
        if message.strip().lower() in {"hi", "hello", "hey", "hey there"}:
            response = "Hi! I'm WonderWise AI. Where would you like to travel?"
            await asyncio.gather(
                asyncio.to_thread(memory_service.save_message, conversation_id, "user", message),
                asyncio.to_thread(memory_service.save_message, conversation_id, "assistant", response),
            )
            yield response
            return

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

        assistant_response = ""
        llm_started_at = time.perf_counter()
        try:
            async with asyncio.timeout(settings.LLM_TIMEOUT_SECONDS):
                async for chunk in llm.astream(prompt_messages):
                    if chunk.content:
                        assistant_response += chunk.content
                        if retrieved:
                            yield chunk.content
        except TimeoutError:
            metrics.increment("llm_timeouts")
            yield "\n\nThe AI model timed out. Please try again with a shorter request."
        else:
            metrics.increment("llm_requests")
            metrics.observe("llm_duration_ms", (time.perf_counter() - llm_started_at) * 1000)

        if not retrieved and assistant_response:
            assistant_response = remove_unverified_currency_amounts(
                assistant_response,
                has_verified_context=False,
            )
            yield assistant_response

        if retrieved:
            citation_text = append_source_citations("", retrieved).lstrip()
            citation_text = citation_text[len("### Sources"):].lstrip()
            if citation_text:
                yield "\n\n### Sources\n" + citation_text
                assistant_response += "\n\n### Sources\n" + citation_text

        if assistant_response:
            await asyncio.to_thread(
                memory_service.save_message,
                conversation_id,
                "assistant",
                assistant_response,
            )


stream_service = StreamService()

