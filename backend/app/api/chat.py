from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.security import get_current_user
from app.database.database import SessionLocal
from app.database.models import Conversation, User
from app.services.chat_service import chat_service
from app.schemas.chat import ChatRequest
from app.services.response_parser import parse_travel_response


router = APIRouter()


@router.post("/chat")
async def chat(data: ChatRequest, user: User = Depends(get_current_user)):
    session = SessionLocal()
    try:
        conversation = (
            session.query(Conversation)
            .filter(Conversation.id == data.conversation_id, Conversation.user_id == user.id)
            .first()
        )
    finally:
        session.close()

    if conversation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")

    response = await chat_service.chat(data.message, conversation.id)

    structured = parse_travel_response(response)
    return {"response": response, "structured": structured.model_dump()}
