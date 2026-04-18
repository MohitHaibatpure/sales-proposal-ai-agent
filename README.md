# Sales Proposal AI Agent

An AI-powered agent that automates end-to-end sales proposal creation — built as an internship project at **SR INDIA**.

## What It Does

- Gathers client context from CRM data (industry, budget, past deals)
- Remembers past proposals across sessions (SQLite memory)
- Generates structured sales proposals
- Simulates an internal approval workflow
- Exports proposals as downloadable PDFs
- Operates via a Copilot-style Streamlit interface

## Tech Stack

| Layer    | Technology |
|----------|------------|
| Frontend | Streamlit  |
| Backend  | FastAPI    |
| Memory   | SQLite     |
| PDF      | ReportLab  |

## How to Run

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the Backend

```bash
uvicorn backend.main:app --reload
```

### 3. Start the Frontend (in a new terminal)

```bash
streamlit run frontend/app.py
```

The Streamlit UI will open at `http://localhost:8501`. The backend runs at `http://localhost:8000`.

## Project Structure

```
sales-proposal-ai-agent/
├── backend/
│   ├── main.py            # FastAPI endpoints
│   ├── agent.py           # Core agent logic & proposal generation
│   ├── crm_mock.py        # Mock CRM data source
│   ├── memory.py          # SQLite-based proposal memory
│   ├── approval_engine.py # Simulated approval workflow
│   └── pdf_export.py      # PDF generation via ReportLab
├── frontend/
│   └── app.py             # Streamlit UI
├── data/
│   ├── proposals.db       # SQLite database (auto-created)
│   └── exports/           # Generated PDFs
├── requirements.txt
└── README.md
```
