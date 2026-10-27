"""
file_manager.py
Smart file type detection with AI-driven application suggestions
and recent-file tracking.
"""

import mimetypes
import os
from datetime import datetime, timedelta

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/files", tags=["Smart File Manager"])

# Mapping: MIME type prefix / extension → suggested application + AI tip
_APP_SUGGESTIONS: dict = {
    ".pdf":  {"app": "PDF Viewer",         "tip": "Open with a PDF reader for best experience."},
    ".csv":  {"app": "Data Explorer",      "tip": "Load into the No-Code ML Workflow for instant analysis."},
    ".xlsx": {"app": "Spreadsheet Editor", "tip": "Consider exporting to CSV for ML pipeline compatibility."},
    ".xls":  {"app": "Spreadsheet Editor", "tip": "Consider exporting to CSV for ML pipeline compatibility."},
    ".docx": {"app": "Word Processor",     "tip": "Use AI Assistant to summarize this document."},
    ".doc":  {"app": "Word Processor",     "tip": "Use AI Assistant to summarize this document."},
    ".txt":  {"app": "Text Editor",        "tip": "Plain text — suitable for log analysis or NLP tasks."},
    ".py":   {"app": "Code Editor",        "tip": "Python file detected — open in your IDE for editing."},
    ".js":   {"app": "Code Editor",        "tip": "JavaScript file — open in a code editor."},
    ".ts":   {"app": "Code Editor",        "tip": "TypeScript file — open in a code editor."},
    ".json": {"app": "JSON Viewer",        "tip": "Structured data — can be fed directly into API endpoints."},
    ".png":  {"app": "Image Viewer",       "tip": "Image file — can be used for computer vision workflows."},
    ".jpg":  {"app": "Image Viewer",       "tip": "Image file — can be used for computer vision workflows."},
    ".jpeg": {"app": "Image Viewer",       "tip": "Image file — can be used for computer vision workflows."},
    ".mp4":  {"app": "Media Player",       "tip": "Video file — consider GPU acceleration for playback."},
    ".mp3":  {"app": "Audio Player",       "tip": "Audio file — low resource consumption expected."},
    ".zip":  {"app": "Archive Manager",    "tip": "Compressed archive — extract before processing."},
}

# Mock recent-file store (in production this would be persisted)
_RECENT_FILES: list = [
    {
        "filename": "dataset_v2.csv",
        "path": "/home/user/datasets/dataset_v2.csv",
        "extension": ".csv",
        "size_kb": 512,
        "last_accessed": (datetime.now() - timedelta(minutes=10)).isoformat(),
        "suggested_app": "Data Explorer",
    },
    {
        "filename": "report_q3.pdf",
        "path": "/home/user/documents/report_q3.pdf",
        "extension": ".pdf",
        "size_kb": 1024,
        "last_accessed": (datetime.now() - timedelta(hours=1)).isoformat(),
        "suggested_app": "PDF Viewer",
    },
    {
        "filename": "train_model.py",
        "path": "/home/user/projects/train_model.py",
        "extension": ".py",
        "size_kb": 8,
        "last_accessed": (datetime.now() - timedelta(hours=2)).isoformat(),
        "suggested_app": "Code Editor",
    },
    {
        "filename": "config.json",
        "path": "/home/user/projects/config.json",
        "extension": ".json",
        "size_kb": 2,
        "last_accessed": (datetime.now() - timedelta(hours=5)).isoformat(),
        "suggested_app": "JSON Viewer",
    },
    {
        "filename": "presentation.docx",
        "path": "/home/user/documents/presentation.docx",
        "extension": ".docx",
        "size_kb": 256,
        "last_accessed": (datetime.now() - timedelta(days=1)).isoformat(),
        "suggested_app": "Word Processor",
    },
]


class InspectRequest(BaseModel):
    filename: str


@router.post("/inspect", summary="Detect file type and get AI app suggestion")
def inspect_file(body: InspectRequest):
    """
    Given a filename, detect its MIME type and return the suggested application
    plus an AI-generated usage tip.
    """
    filename = body.filename
    ext = os.path.splitext(filename)[-1].lower()
    mime_type, _ = mimetypes.guess_type(filename)

    suggestion = _APP_SUGGESTIONS.get(
        ext,
        {"app": "Default System Viewer", "tip": "No specific recommendation available for this file type."},
    )

    return {
        "filename": filename,
        "extension": ext,
        "mime_type": mime_type or "application/octet-stream",
        "suggested_application": suggestion["app"],
        "ai_tip": suggestion["tip"],
    }


@router.get("/recent", summary="List recently accessed files")
def get_recent_files():
    """Return the 5 most recently accessed files with metadata and app suggestions."""
    return {
        "count": len(_RECENT_FILES),
        "files": _RECENT_FILES,
    }
