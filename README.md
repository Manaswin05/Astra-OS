# Astra-OS Backend

> An AI-native operating environment backend — resource monitoring, no-code ML pipelines, smart file management, and a natural language assistant, all served over a REST API and an interactive CLI.

---

## Quick Start

### 1. Set up the environment

```bat
build.bat
```

This creates a virtual environment in `venv/`, activates it, and installs all dependencies from `requirements.txt`.

If you prefer doing it manually:

```bat
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```

---

### 2. Run the API server

```bat
venv\Scripts\activate.bat
uvicorn main:app --reload --port 8000
```

Once running:
- API root / health check → `http://localhost:8000/`
- Interactive Swagger docs → `http://localhost:8000/docs`

---

### 3. Run the CLI simulator

```bat
venv\Scripts\activate.bat
python cli.py
```

> **Note:** `start.bat` currently calls `manage.py` (the old filename). Update it to `python cli.py` after the rename.

This launches an interactive UNIX-like shell that simulates an in-memory filesystem. Type `help` inside the shell to see all available commands.

---

## Project Structure

```
backend/
├── main.py                        # FastAPI app — entry point for the API server
├── cli.py                         # Interactive CLI OS simulator (renamed from manage.py)
├── requirements.txt               # Python dependencies
├── build.bat                      # Setup: creates venv and installs dependencies
├── start.bat                      # Shortcut to launch CLI (needs update to cli.py)
│
├── modules/
│   ├── __init__.py
│   ├── resource_monitor.py        # CPU, RAM, Disk, GPU monitoring + recommendations
│   ├── ml_workflow.py             # No-code ML pipeline: upload → clean → train
│   ├── file_manager.py            # File type detection + app suggestions
│   ├── ai_assistant.py            # Rule-based intent parser (NLP → action)
│   └── workflow_planner.py        # Goal → step-by-step execution plan
│
└── Docs/
    ├── CODEBASE_DOCUMENTATION.md  # Full architecture, disconnections, and issue tracker
    ├── CLI_COMMANDS.md            # Complete CLI command reference
    ├── Astra-OS.pdf
    └── The_Agentic_OS_Blueprint.pdf
```

---

## What Each Part Does

| Component | How to run | Purpose |
|-----------|------------|---------|
| `main.py` | `uvicorn main:app --reload` | REST API — exposes all modules as HTTP endpoints |
| `cli.py` | `python cli.py` | Standalone interactive CLI with an in-memory virtual filesystem |
| `modules/resource_monitor.py` | (via API) | Real-time CPU, RAM, disk, GPU stats and optimization tips |
| `modules/ml_workflow.py` | (via API) | Upload a CSV, auto-clean it, train a RandomForest model |
| `modules/file_manager.py` | (via API) | Detect file type, suggest the right app to open it |
| `modules/ai_assistant.py` | (via API) | Parse natural language and map it to an Astra-OS action |
| `modules/workflow_planner.py` | (via API) | Turn a free-text goal into a structured step-by-step plan |

---

## API Overview

All endpoints are served at `http://localhost:8000`. See `http://localhost:8000/docs` for the full interactive reference.

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/resources/status` | Full system resource snapshot |
| GET | `/resources/cpu` | Per-core CPU usage |
| GET | `/resources/optimize` | AI-driven optimization recommendations |
| POST | `/ml/upload` | Upload a CSV dataset |
| POST | `/ml/clean` | Auto-clean the uploaded dataset |
| POST | `/ml/train` | Train a model on cleaned data |
| GET | `/ml/status` | Current ML pipeline state |
| POST | `/files/inspect` | Detect file type and get app suggestion |
| GET | `/files/recent` | List recently accessed files |
| POST | `/assistant/intent` | Parse a natural language message to intent |
| GET | `/assistant/suggestions` | Get quick-action suggestions |
| POST | `/workflow/plan` | Convert a goal string to an execution plan |
| GET | `/workflow/templates` | List all pre-built workflow templates |

---

## Dependencies

| Package | Version | Used by |
|---------|---------|---------|
| fastapi | 0.111.0 | main.py, all modules |
| uvicorn | 0.29.0 | API server runner |
| psutil | 5.9.8 | resource_monitor.py |
| scikit-learn | 1.4.2 | ml_workflow.py |
| pandas | 2.2.2 | ml_workflow.py |
| python-multipart | 0.0.9 | ml_workflow.py (file uploads) |
| GPUtil | optional | resource_monitor.py (GPU stats) |

Install GPUtil separately if GPU monitoring is needed:
```bat
pip install gputil
```

---

## Documentation

- `Docs/CODEBASE_DOCUMENTATION.md` — Full architecture breakdown, file-by-file reference, known disconnections and bugs, data flow diagrams, and recommended fixes.
- `Docs/CLI_COMMANDS.md` — Complete command reference for `cli.py` with syntax, examples, and error behaviours.

---

## Known Issues

The CLI (`cli.py`) and the API (`main.py`) are currently **two separate programs with no shared state**. Files created in the CLI do not interact with the API, and vice versa. See `Docs/CODEBASE_DOCUMENTATION.md` section 6 for the full list of disconnections and recommended fixes.
