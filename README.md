# Astra-OS 🧠

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688?logo=fastapi)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Prototype-orange)

> **An AI-native operating environment that understands user intent, automatically optimizes hardware resources, and enables no-code AI development on everyday computers.**

---

## Table of Contents

- [Problem Statement](#problem-statement)
- [Solution](#solution)
- [System Architecture](#system-architecture)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Endpoints](#api-endpoints)
- [Roadmap](#roadmap)
- [Research References](#research-references)
- [Contributing](#contributing)
- [License](#license)

---

## Problem Statement

Current operating systems are designed for general-purpose computing, not AI workloads. Users must:

- Install and configure multiple ML tools manually
- Write boilerplate code for every experiment
- Manage CPU/GPU/RAM resources by hand
- Tune memory and troubleshoot environment failures

This makes AI development unnecessarily difficult, especially on low-resource hardware.

---

## Solution

Astra-OS introduces an **AI Orchestration Layer** that sits above the traditional OS. Instead of the user managing the computer, the AI manages it for them — translating high-level goals into optimized, automated workflows.

---

## System Architecture

```
┌─────────────────────────────────────────────────┐
│                     User                        │
└───────────────────────┬─────────────────────────┘
                        │ Goal / Intent
┌───────────────────────▼─────────────────────────┐
│               AI Assistant Layer                │
│         (Intent Parser + Suggestions)           │
└───────────────────────┬─────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────┐
│             Workflow Planner                    │
│     (Goal → Step-by-step execution plan)        │
└───────────────────────┬─────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────┐
│            Resource Optimizer                   │
│    CPU Manager │ GPU Manager │ RAM │ Storage     │
└───────────────────────┬─────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────┐
│            Operating System / Hardware          │
└─────────────────────────────────────────────────┘
```

---

## Key Features

| Module | Description |
|---|---|
| **AI Assistant** | Rule-based intent parser that maps natural language to OS actions |
| **Resource Optimizer** | Real-time CPU, GPU, RAM, and Disk monitoring with optimization recommendations |
| **No-Code ML Workflow** | Upload CSV → auto-clean → train → evaluate → export, zero code required |
| **Smart File Manager** | Detects file type, suggests the right application, tracks recent files |
| **Workflow Planner** | Translates a user goal string into an ordered, module-mapped execution plan |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI 0.111.0 |
| Server | Uvicorn 0.29.0 |
| System Monitoring | psutil 5.9.8 |
| Machine Learning | scikit-learn 1.4.2 |
| Data Processing | pandas 2.2.2 |
| File Uploads | python-multipart 0.0.9 |
| Language | Python 3.10+ |

---

## Project Structure

```
Astra-OS/
├── README.md
├── Docs/
│   ├── Astra-OS.pdf
│   └── The_Agentic_OS_Blueprint.pdf
└── backend/
    ├── main.py                    # FastAPI application entry point
    ├── requirements.txt           # Pinned dependencies
    └── modules/
        ├── __init__.py
        ├── resource_monitor.py    # CPU / RAM / Disk / GPU stats & recommendations
        ├── ml_workflow.py         # No-code ML pipeline (upload → train → evaluate)
        ├── file_manager.py        # Smart file type detection & recent files
        ├── ai_assistant.py        # Intent parser & quick-action suggestions
        └── workflow_planner.py    # Goal → execution plan mapper
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/<your-username>/Astra-OS.git
cd Astra-OS/backend

# Install dependencies
pip install -r requirements.txt

# Start the backend server
uvicorn main:app --reload --port 8000
```

The API will be live at **http://localhost:8000**  
Interactive docs: **http://localhost:8000/docs**

---

## API Endpoints

### Health
| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |

### Resource Monitor
| Method | Endpoint | Description |
|---|---|---|
| GET | `/resources/status` | Full system resource snapshot |
| GET | `/resources/cpu` | Per-core CPU usage |
| GET | `/resources/optimize` | AI-generated optimization recommendations |

### No-Code ML Workflow
| Method | Endpoint | Description |
|---|---|---|
| POST | `/ml/upload` | Upload a CSV dataset |
| POST | `/ml/clean` | Auto-clean the uploaded dataset |
| POST | `/ml/train` | Train a model on cleaned data |
| GET | `/ml/status` | Current pipeline step and results |

### Smart File Manager
| Method | Endpoint | Description |
|---|---|---|
| POST | `/files/inspect` | Detect file type and get AI app suggestion |
| GET | `/files/recent` | List recently accessed files |

### AI Assistant
| Method | Endpoint | Description |
|---|---|---|
| POST | `/assistant/intent` | Parse natural language to intent + action |
| GET | `/assistant/suggestions` | Get 3 contextual quick-action suggestions |

### Workflow Planner
| Method | Endpoint | Description |
|---|---|---|
| POST | `/workflow/plan` | Convert a goal string to a step-by-step plan |
| GET | `/workflow/templates` | List pre-built workflow templates |

---

## Roadmap

| Phase | Goal |
|---|---|
| **Phase 1** | Core backend: resource monitor, intent parser, basic ML pipeline |
| **Phase 2** | Local LLM integration for smarter intent understanding |
| **Phase 3** | Desktop GUI / web dashboard for no-code interactions |
| **Phase 4** | Multi-agent collaboration and autonomous scheduling |
| **Phase 5** | Enterprise AI workstation platform with plugin ecosystem |

---

## Research References

### IEEE Papers

1. **AI-Empowered Fog/Edge Resource Management for IoT Applications**  
   *IEEE Communications Surveys & Tutorials, 2024*  
   https://ieeexplore.ieee.org/document/10335918

2. **A Comprehensive Review of AI Techniques for Resource Management in Fog Computing**  
   *IEEE Access, 2024*  
   https://ieeexplore.ieee.org/document/10627948

3. **Edge-LLM: A Collaborative Framework for Large Language Model Serving in Edge Computing**  
   *IEEE ICWS, 2024*  
   https://ieeexplore.ieee.org/document/10707514

4. **Distributed AI in Zero-Touch Provisioning for Edge Networks**  
   *IEEE Computer, 2024*  
   https://ieeexplore.ieee.org/document/1046168

5. **Decentralized Scheduling and Dynamic Pricing for Edge Computing**  
   *IEEE/ACM Transactions on Networking*  
   https://ieeexplore.ieee.org/document/9903403

### arXiv Papers

6. **AIOS: LLM Agent Operating System**  
   Closest existing research — introduces AI kernel, agent scheduler, context/memory/tool management. Achieves up to 2.1× faster execution.  
   https://arxiv.org/abs/2403.16971

7. **LLM as OS, Agents as Apps**  
   Frames the LLM as the operating system and agents as applications.  
   https://arxiv.org/abs/2312.03815

8. **Semantic File System for AIOS**  
   Intelligent file opening by semantic understanding rather than filename/folder only.  
   https://arxiv.org/abs/2410.11843

9. **AgentRM: An OS-Inspired Resource Manager for LLM Agent Systems**  
   Applies OS concepts (scheduling, memory management) to improve agent execution.  
   https://arxiv.org/abs/2603.13110

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Commit your changes: `git commit -m 'feat: add your feature'`
4. Push to the branch: `git push origin feat/your-feature`
5. Open a Pull Request

Please follow [Conventional Commits](https://www.conventionalcommits.org/) for commit messages.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

*Astra-OS — Because computers should work for you, not the other way around.*
