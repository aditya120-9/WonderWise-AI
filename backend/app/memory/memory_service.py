from typing import List
from app.database.database import SessionLocal
from app.database.models import Message

class MemoryService:

    def save_message(self, conversation_id: int, role: str, content: str):
        session = SessionLocal()
        try:
            message = Message(conversation_id=conversation_id, role=role, content=content)
            session.add(message)
            session.commit()
            return message.id
        finally:
            session.close()

    def load_recent(self, conversation_id: int, limit: int = 10) -> List[Message]:
        session = SessionLocal()
        try:
            return (
                session.query(Message)
                .filter(Message.conversation_id == conversation_id)
                .order_by(Message.created_at.desc())
                .limit(limit)
                .all()
            )
        finally:
            session.close()

memory_service = MemoryService()
