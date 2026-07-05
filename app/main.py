# pyrefly: ignore [missing-import]
from fastapi import FastAPI
from app.api.message import router as message_router

# Initialize the FastAPI application
app = FastAPI(
    title="AI Communication Agent",
    description="An AI agent that generates platform-specific messages.",
    version="0.1.0"
)

app.include_router(
    message_router,
    prefix="/api/v1"
)

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify that the application is running.
    """
    return {
        "status": "ok",
        "project": "AI Communication Agent",
        "version": "0.1.0"
    }
