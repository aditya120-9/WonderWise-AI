from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from app.llm.ollama_client import llm
from app.prompts.system_prompt import SYSTEM_PROMPT
from app.rag.retriever import retrieve
from app.memory.memory_service import memory_service


class StreamService:

    async def stream(self, message: str, conversation_id: int = 1):
        if message.strip().lower() in {"hi", "hello", "hey", "hey there"}:
            response = "Hi! I'm WonderWise AI. Where would you like to travel?"
            memory_service.save_message(conversation_id, "user", message)
            memory_service.save_message(conversation_id, "assistant", response)
            yield response
            return

        # Keep the prompt lightweight for fast local inference without losing relevant context.
        retrieved = retrieve(message, n_results=1)

        context_text = ""
        if retrieved:
            blocks = []
            for item in retrieved:
                source = item["metadata"].get("source", "unknown")
                doc = item.get("document", "")
                doc = doc[:650]
                blocks.append(f"Source: {source}\n{doc}")

            context_text = "\n\n".join(blocks)[:1200]

        history_items = memory_service.load_recent(conversation_id, limit=3)

        prompt_messages = [SystemMessage(content=SYSTEM_PROMPT)]
        if context_text:
            prompt_messages.append(HumanMessage(content=f"Context:\n{context_text}"))

        for item in reversed(history_items):
            if item.role == "assistant":
                prompt_messages.append(AIMessage(content=item.content))
            else:
                prompt_messages.append(HumanMessage(content=item.content))

        prompt_messages.append(HumanMessage(content=message))
        memory_service.save_message(conversation_id, "user", message)

        assistant_response = ""
        async for chunk in llm.astream(prompt_messages):
            if chunk.content:
                assistant_response += chunk.content
                yield chunk.content

        if assistant_response:
            memory_service.save_message(conversation_id, "assistant", assistant_response)


stream_service = StreamService()

