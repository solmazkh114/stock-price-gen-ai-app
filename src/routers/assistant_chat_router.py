from ..handlers.chat_handler import ChatRequest, chat_handler
from fastapi import APIRouter

assistant_chat_router = APIRouter()

@assistant_chat_router.post("/chat")
def chat(request: ChatRequest): return chat_handler(request)