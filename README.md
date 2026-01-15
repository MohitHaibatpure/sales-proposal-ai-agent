# Sales Proposal AI Agent (Copilot-Style)

## Overview
This project demonstrates a working AI agent for enterprise sales proposal
generation, inspired by Microsoft 365 Copilot extensibility.

The agent:
- Gathers context from CRM systems
- Remembers past proposals
- Drafts structured proposals
- Simulates internal approvals
- Operates via a Copilot-like interface

## Tech Stack
- Frontend: Streamlit
- Backend: FastAPI
- Memory: SQLite
- Agent Logic: Python

## How to Run

### Backend
```bash
uvicorn backend.main:app --reload
