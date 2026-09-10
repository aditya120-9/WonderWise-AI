from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.security import get_current_user
from app.database.database import SessionLocal
from app.database.models import Conversation, User
from app.schemas.conversation import ConversationCreate, ConversationResponse, ConversationUpdate

router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.get("", response_model=list[ConversationResponse])
async def list_conversations(user: User = Depends(get_current_user)):
    session = SessionLocal()
    try:
        return (
            session.query(Conversation)
            .filter(Conversation.user_id == user.id)
            .order_by(Conversation.created_at.desc())
            .all()
        )
    finally:
        session.close()


@router.post("", response_model=ConversationResponse, status_code=201)
async def create_conversation(
    data: ConversationCreate,
    user: User = Depends(get_current_user),
):
    session = SessionLocal()
    try:
        conversation = Conversation(user_id=user.id, title=data.title.strip())
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation
    finally:
        session.close()


def _owned_conversation(session, conversation_id: int, user_id: int) -> Conversation:
    conversation = (
        session.query(Conversation)
        .filter(Conversation.id == conversation_id, Conversation.user_id == user_id)
        .first()
    )
    if conversation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    return conversation


@router.patch("/{conversation_id}", response_model=ConversationResponse)
async def rename_conversation(
    conversation_id: int,
    data: ConversationUpdate,
    user: User = Depends(get_current_user),
):
    session = SessionLocal()
    try:
        conversation = _owned_conversation(session, conversation_id, user.id)
        conversation.title = data.title.strip()
        session.commit()
        session.refresh(conversation)
        return conversation
    finally:
        session.close()


@router.delete("/{conversation_id}", status_code=204)
async def delete_conversation(conversation_id: int, user: User = Depends(get_current_user)):
    session = SessionLocal()
    try:
        conversation = _owned_conversation(session, conversation_id, user.id)
        session.delete(conversation)
        session.commit()
    finally:
        session.close()