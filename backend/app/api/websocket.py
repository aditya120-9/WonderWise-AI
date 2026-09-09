from fastapi import APIRouter, WebSocket, WebSocketDisconnect  # type: ignore
from app.services.stream_service import stream_service
import json

router = APIRouter()


@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            payload = await websocket.receive_text()

            conversation_id = 1
            request_id = None
            message = payload

            try:
                parsed = json.loads(payload)
                if isinstance(parsed, dict):
                    message = parsed.get("message", payload)
                    conversation_id = parsed.get("conversation_id", 1)
                    request_id = parsed.get("request_id")
            except json.JSONDecodeError:
                message = payload

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

