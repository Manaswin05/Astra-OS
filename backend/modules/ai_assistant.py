"""
ai_assistant.py
Rule-based intent parser that maps natural language to Astra-OS actions.
No external API or LLM key required — works fully offline.
"""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/assistant", tags=["AI Assistant"])

# Intent rules: each entry is (keywords, intent_label, suggested_action, base_confidence)
_INTENT_RULES: list[tuple] = [
    (
        {"train", "model", "dataset", "csv", "ml", "machine learning", "classify", "predict", "regression"},
        "ml_workflow",
        "Launch the No-Code ML Workflow pipeline.",
        0.92,
    ),
    (
        {"cpu", "ram", "memory", "gpu", "optimize", "resource", "performance", "slow", "lag", "usage"},
        "resource_optimize",
        "Run the Resource Optimizer and apply recommendations.",
        0.90,
    ),
    (
        {"open", "file", "document", "pdf", "spreadsheet", "recent", "resume", "read"},
        "file_manager",
        "Use the Smart File Manager to open the file with the best application.",
        0.88,
    ),
    (
        {"workflow", "plan", "automate", "task", "goal", "steps", "pipeline"},
        "workflow_planner",
        "Generate a step-by-step workflow plan for your goal.",
        0.85,
    ),
    (
        {"help", "what", "how", "explain", "show", "tell", "can you", "?"},
        "general_help",
        "I can help with ML workflows, resource optimization, file management, and task automation.",
        0.75,
    ),
]


def _parse_intent(message: str) -> dict:
    """Match the message against intent rules and return the best match."""
    lower = message.lower()
    words = set(lower.split())

    best_intent = "unknown"
    best_action = "Please rephrase your request or type 'help' to see available actions."
    best_confidence = 0.0

    for keywords, intent, action, confidence in _INTENT_RULES:
        # Count matching keywords (including partial substring matches)
        matches = sum(1 for kw in keywords if kw in lower)
        if matches > 0:
            # Scale confidence by match density
            scaled = confidence * min(1.0, matches / max(1, len(keywords) * 0.3))
            if scaled > best_confidence:
                best_confidence = round(scaled, 2)
                best_intent = intent
                best_action = action

    return {
        "intent": best_intent,
        "action": best_action,
        "confidence": best_confidence,
    }


class IntentRequest(BaseModel):
    message: str


@router.post("/intent", summary="Parse natural language to intent + action")
def parse_intent(body: IntentRequest):
    """
    Accept a natural language message and return the detected intent,
    suggested action, and confidence score.

    Example intents:
    - "train a model on my dataset" → ml_workflow
    - "my cpu is running slow" → resource_optimize
    - "open my resume file" → file_manager
    - "help me plan my workflow" → workflow_planner
    """
    if not body.message.strip():
        return {
            "intent": "unknown",
            "action": "Please provide a message.",
            "confidence": 0.0,
        }

    result = _parse_intent(body.message)
    result["original_message"] = body.message
    return result


@router.get("/suggestions", summary="Get contextual quick-action suggestions")
def get_suggestions():
    """Return 3 quick-action suggestions the user can take right now."""
    return {
        "suggestions": [
            {
                "id": 1,
                "label": "Analyze system resources",
                "description": "Check your CPU, RAM, and Disk usage and get optimization tips.",
                "endpoint": "GET /resources/optimize",
                "icon": "⚡",
            },
            {
                "id": 2,
                "label": "Start a no-code ML workflow",
                "description": "Upload a CSV dataset and train a model in minutes — no coding needed.",
                "endpoint": "POST /ml/upload",
                "icon": "🤖",
            },
            {
                "id": 3,
                "label": "Smart file open",
                "description": "Let Astra-OS detect your file type and recommend the best application.",
                "endpoint": "POST /files/inspect",
                "icon": "📂",
            },
        ]
    }
