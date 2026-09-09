import importlib

try:
    APIRouter = importlib.import_module("fastapi").APIRouter
except ImportError:
    class APIRouter:
        def __init__(self, *args, **kwargs):
            pass

        def post(self, *args, **kwargs):
            def decorator(func):
                return func

            return decorator

try:
    BaseModel = importlib.import_module("pydantic").BaseModel
except ImportError:
    class BaseModel:
        pass

from app.services.chat_service import chat_service


router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    conversation_id: int = 1


@router.post("/chat")
async def chat(data: ChatRequest):
    response = await chat_service.chat(data.message, data.conversation_id)

    return {"response": response}
