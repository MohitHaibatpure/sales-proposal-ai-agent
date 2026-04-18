import os
import requests
from dotenv import load_dotenv

# Load API key from .env
load_dotenv(override=True)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def simulate_approval(proposal: str) -> str:
    """Simulates internal approval based on content."""
    if "budget" in proposal.lower() or "pricing" in proposal.lower():
        return "Approved by Sales Manager"
    return "Needs Review - Missing Budget Info"

def generate_proposal(client: str, use_case: str) -> str:
    """
    Uses Google Gemini via REST API to generate a tailored sales proposal.
    Dynamically assumes timeline and realistic pricing since no CRM is attached.
    """

    prompt = f"""You are an expert enterprise sales consultant. Generate a highly professional, 
detailed sales proposal for the following deal:

CLIENT: {client}
CLIENT REQUIREMENT:
{use_case}

Based strictly on this requirement, intelligently infer the industry and scale of the project.
Generate a structured sales proposal with these sections:
1. Executive Summary
2. Client Context & Project Understanding
3. Proposed Solution
4. Business Value & Expected ROI
5. Implementation Approach
6. Pricing Estimate (Intelligently estimate a realistic budget based on the scope of their requirement)
7. Next Steps

Make the proposal specific, actionable, and highly professional. 
Tailor the solution directly to what the client asked for. Do NOT use generic placeholder text.
Keep it concise but impactful (around 400-500 words)."""

    try:
        # 1. Primary AI: Google Gemini API
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
        payload = {"contents": [{"parts":[{"text": prompt}]}]}
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(url, json=payload, headers=headers, timeout=45)
        response.raise_for_status()
        
        return response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        
    except Exception as gemini_err:
        try:
            # 2. Secondary AI: Free Unauthenticated API (Pollinations)
            print(f"Gemini failed ({gemini_err}). Switching to secondary Free AI fallback...")
            fallback_url = "https://text.pollinations.ai/"
            fallback_payload = {
                "messages": [
                    {"role": "system", "content": "You are an expert sales proposal generator."},
                    {"role": "user", "content": prompt}
                ]
            }
            fallback_response = requests.post(fallback_url, json=fallback_payload, timeout=45)
            fallback_response.raise_for_status()
            
            return fallback_response.text.strip()
            
        except Exception as e:
            # Absolute worst-case scenario
            return f"[AI Error: Both Primary and Secondary AI APIs failed. Err: {e}]\n\nFallback Proposal for {client}:\nRequirement: {use_case}\n(Due to system failure, we could not generate the AI content)"

def run_agent(client: str, use_case: str) -> dict:
    """Main agent entry point orchestrating proposal generation and approval."""
    proposal = generate_proposal(client, use_case)
    approval_status = simulate_approval(proposal)

    return {
        "proposal": proposal,
        "approval_status": approval_status
    }
