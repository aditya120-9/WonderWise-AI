from fastapi import APIRouter, WebSocket, WebSocketDisconnect  # type: ignore
from app.auth.security import get_user_from_token
from app.database.database import SessionLocal
from app.database.models import Conversation
from app.config.settings import settings
from app.security.rate_limit import allow_request
from app.services.stream_service import stream_service
import json

router = APIRouter()


@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    client_host = websocket.client.host if websocket.client else "unknown"
    allowed, retry_after = allow_request(f"websocket:{client_host}", settings.CHAT_RATE_LIMIT_REQUESTS)
    if not allowed:
        await websocket.close(code=1013, reason=f"Rate limited. Retry in {retry_after}s")
        return
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008, reason="Authentication required")
        return

    try:
        user = get_user_from_token(token)
    except Exception:
        await websocket.close(code=1008, reason="Invalid or expired token")
        return

    await websocket.accept()

    try:
        while True:
            payload = await websocket.receive_text()

            conversation_id = None
            request_id = None
            message = payload

            try:
                parsed = json.loads(payload)
                if isinstance(parsed, dict):
                    message = parsed.get("message", payload)
                    conversation_id = parsed.get("conversation_id")
                    request_id = parsed.get("request_id")
            except json.JSONDecodeError:
                message = payload

            if not isinstance(conversation_id, int):
                await websocket.send_text(json.dumps({"type": "error", "message": "conversation_id is required", "request_id": request_id}))
                continue

            session = SessionLocal()
            try:
                conversation = (
                    session.query(Conversation)
                    .filter(Conversation.id == conversation_id, Conversation.user_id == user.id)
                    .first()
                )
            finally:
                session.close()

            if conversation is None:
                await websocket.send_text(json.dumps({"type": "error", "message": "Conversation not found", "request_id": request_id}))
                continue

            # stream_service yields token chunks; keep them tied to request_id
            async for token in stream_service.stream(
                message,
                conversation_id=conversation_id,
            ):
                await websocket.send_text(
                    json.dumps(
                        {
                            "type": "chunk",
                            "content": token,
                            "request_id": request_id,
                        }
                    )
                )

            await websocket.send_text(
                json.dumps({"type": "end", "request_id": request_id})
            )

    except WebSocketDisconnect:
        print("Client disconnected")

    except Exception as e:
        await websocket.send_text(
            json.dumps(
                {
                    "type": "error",
                    "message": str(e),
                }
            )
        )

