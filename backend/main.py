from fastapi import FastAPI
from fastapi.responses import FileResponse
from backend.agent import run_agent
from backend.memory import load_memory
from backend.pdf_export import generate_proposal_pdf

app = FastAPI(title="Sales Proposal AI Agent")


@app.post("/run-agent")
def run(payload: dict):
    return run_agent(payload)


@app.get("/memory/{client}")
def get_memory(client: str):
    memory = load_memory(client)
    return {
        "client": client,
        "past_proposals": [m[0] for m in memory]
    }


@app.post("/export-pdf")
def export_pdf(payload: dict):
    proposal_text = payload.get("proposal")

    pdf_path = generate_proposal_pdf(proposal_text)

    return FileResponse(
        path=pdf_path,
        filename="Sales_Proposal.pdf",
        media_type="application/pdf"
    )
