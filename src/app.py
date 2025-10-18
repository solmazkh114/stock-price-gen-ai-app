from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from .routers.assistant_chat_router import assistant_chat_router



logger.info("app starting...")
app = FastAPI(title="Welcome to Stock Price Assistant API")

logger.info("Adding CORS middleware...")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("Defining routes...")

@app.get("/health")
async def health_check():
    """Health check endpoint for load balancer"""
    return {"status": "healthy", "service": "stock-price-assistant"}

app.include_router(assistant_chat_router, prefix="")