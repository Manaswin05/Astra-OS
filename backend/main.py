"""
main.py
Astra-OS Backend — FastAPI entry point.

Start the server:
    uvicorn main:app --reload --port 8000

Interactive API docs:
    http://localhost:8000/docs
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from modules.ai_assistant import router as assistant_router
from modules.file_manager import router as file_router
from modules.ml_workflow import router as ml_router
from modules.resource_monitor import router as resource_router
from modules.workflow_planner import router as workflow_router

app = FastAPI(
    title="Astra-OS API",
    description=(
        "Backend for Astra-OS — an AI-native operating environment that understands "
        "user intent, optimizes hardware resources, and enables no-code ML development."
    ),
    version="0.1.0",
    contact={
        "name": "Astra-OS",
        "url": "https://github.com/your-username/Astra-OS",
    },
    license_info={"name": "MIT"},
)

# Allow all origins in development; restrict in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all module routers
app.include_router(resource_router)
app.include_router(ml_router)
app.include_router(file_router)
app.include_router(assistant_router)
app.include_router(workflow_router)


@app.get("/", tags=["Health"], summary="Health check")
def health_check():
    """Confirm the Astra-OS backend is running."""
    return {
        "status": "ok",
        "service": "Astra-OS Backend",
        "version": "0.1.0",
        "docs": "/docs",
        "modules": [
            "resource_monitor",
            "ml_workflow",
            "file_manager",
            "ai_assistant",
            "workflow_planner",
        ],
    }
