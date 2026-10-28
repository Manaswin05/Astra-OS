"""
workflow_planner.py
Maps a user goal string to an ordered, module-mapped execution plan.
Includes pre-built templates for the most common Astra-OS workflows.
"""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/workflow", tags=["Workflow Planner"])

# Pre-built workflow templates
_TEMPLATES: list[dict] = [
    {
        "id": "ml_training",
        "name": "No-Code ML Training",
        "description": "End-to-end machine learning from raw CSV to trained model.",
        "trigger_keywords": ["train", "ml", "dataset", "model", "predict", "classify"],
        "steps": [
            {"step": 1, "action": "Upload CSV dataset",                 "module": "ml_workflow",       "endpoint": "POST /ml/upload",          "status": "pending"},
            {"step": 2, "action": "Analyze dataset structure",          "module": "ml_workflow",       "endpoint": "POST /ml/upload",          "status": "pending"},
            {"step": 3, "action": "Auto-detect missing values",         "module": "ml_workflow",       "endpoint": "POST /ml/clean",           "status": "pending"},
            {"step": 4, "action": "Clean and preprocess data",          "module": "ml_workflow",       "endpoint": "POST /ml/clean",           "status": "pending"},
            {"step": 5, "action": "Select target column",               "module": "ml_workflow",       "endpoint": "POST /ml/train",           "status": "pending"},
            {"step": 6, "action": "Auto-select best model type",        "module": "ml_workflow",       "endpoint": "POST /ml/train",           "status": "pending"},
            {"step": 7, "action": "Train and evaluate model",           "module": "ml_workflow",       "endpoint": "POST /ml/train",           "status": "pending"},
            {"step": 8, "action": "Review accuracy and feature scores", "module": "ml_workflow",       "endpoint": "GET /ml/status",           "status": "pending"},
        ],
    },
    {
        "id": "resource_optimization",
        "name": "Resource Optimization",
        "description": "Monitor system health and apply AI-recommended optimizations.",
        "trigger_keywords": ["optimize", "cpu", "ram", "memory", "performance", "slow", "resource"],
        "steps": [
            {"step": 1, "action": "Collect full system resource snapshot", "module": "resource_monitor", "endpoint": "GET /resources/status",   "status": "pending"},
            {"step": 2, "action": "Analyze per-core CPU usage",            "module": "resource_monitor", "endpoint": "GET /resources/cpu",      "status": "pending"},
            {"step": 3, "action": "Generate optimization recommendations",  "module": "resource_monitor", "endpoint": "GET /resources/optimize", "status": "pending"},
            {"step": 4, "action": "Apply resource scheduling decisions",    "module": "resource_monitor", "endpoint": "GET /resources/optimize", "status": "pending"},
            {"step": 5, "action": "Confirm system stability",               "module": "resource_monitor", "endpoint": "GET /resources/status",   "status": "pending"},
        ],
    },
    {
        "id": "smart_file_open",
        "name": "Smart File Open",
        "description": "Intelligently open a file using the best available application.",
        "trigger_keywords": ["open", "file", "document", "read", "resume", "pdf", "csv"],
        "steps": [
            {"step": 1, "action": "Receive file open request",          "module": "ai_assistant",  "endpoint": "POST /assistant/intent",   "status": "pending"},
            {"step": 2, "action": "Detect file type and MIME",          "module": "file_manager",  "endpoint": "POST /files/inspect",      "status": "pending"},
            {"step": 3, "action": "Check user's recent file history",   "module": "file_manager",  "endpoint": "GET /files/recent",        "status": "pending"},
            {"step": 4, "action": "Select best application for file",   "module": "file_manager",  "endpoint": "POST /files/inspect",      "status": "pending"},
            {"step": 5, "action": "Open file with recommended app",     "module": "file_manager",  "endpoint": "POST /files/inspect",      "status": "pending"},
        ],
    },
]

_GENERIC_PLAN: list[dict] = [
    {"step": 1, "action": "Parse user intent",              "module": "ai_assistant",    "endpoint": "POST /assistant/intent",    "status": "pending"},
    {"step": 2, "action": "Generate workflow plan",         "module": "workflow_planner","endpoint": "POST /workflow/plan",       "status": "pending"},
    {"step": 3, "action": "Check system resources",         "module": "resource_monitor","endpoint": "GET /resources/status",    "status": "pending"},
    {"step": 4, "action": "Execute planned steps",          "module": "ai_assistant",    "endpoint": "GET /assistant/suggestions","status": "pending"},
    {"step": 5, "action": "Verify and report outcome",      "module": "ai_assistant",    "endpoint": "GET /assistant/suggestions","status": "pending"},
]


def _find_template(goal: str) -> dict | None:
    lower = goal.lower()
    for template in _TEMPLATES:
        if any(kw in lower for kw in template["trigger_keywords"]):
            return template
    return None


class PlanRequest(BaseModel):
    goal: str


@router.post("/plan", summary="Convert a goal string to a step-by-step plan")
def generate_plan(body: PlanRequest):
    """
    Accept a free-text goal and return a structured, step-by-step execution plan
    mapping each step to its module and API endpoint.

    Examples:
    - "I want to train a model on my dataset"   → ML Training plan
    - "My computer is running slow"             → Resource Optimization plan
    - "Open my resume file"                     → Smart File Open plan
    """
    if not body.goal.strip():
        return {"error": "Goal cannot be empty."}

    template = _find_template(body.goal)

    if template:
        return {
            "goal": body.goal,
            "matched_template": template["name"],
            "description": template["description"],
            "total_steps": len(template["steps"]),
            "plan": template["steps"],
        }

    return {
        "goal": body.goal,
        "matched_template": "Generic AI Assistant Plan",
        "description": "No specific workflow matched. Using the general AI assistant flow.",
        "total_steps": len(_GENERIC_PLAN),
        "plan": _GENERIC_PLAN,
    }


@router.get("/templates", summary="List pre-built workflow templates")
def get_templates():
    """Return all available pre-built workflow templates."""
    return {
        "count": len(_TEMPLATES),
        "templates": [
            {
                "id": t["id"],
                "name": t["name"],
                "description": t["description"],
                "total_steps": len(t["steps"]),
                "trigger_keywords": t["trigger_keywords"],
            }
            for t in _TEMPLATES
        ],
    }
