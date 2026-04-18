import os
import requests
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def fetch_crm_data(client_name: str) -> dict:
    """Mock CRM database lookup."""
    mock_crm = {
        "Acme Corp": {
            "industry": "Manufacturing",
            "budget": "$120,000",
            "past_deals": ["ERP Upgrade", "Supply Chain Optimization"]
        },
        "Northstar Retail": {
            "industry": "Retail",
            "budget": "$75,000",
            "past_deals": ["AI Demand Forecasting"]
        }
    }
    return mock_crm.get(client_name, {
        "industry": "Unknown",
        "budget": "Not Disclosed",
        "past_deals": []
    })

def simulate_approval(proposal: str) -> str:
    """Simulates internal approval based on content."""
    if "budget" in proposal.lower() or "pricing" in proposal.lower():
        return "Approved by Sales Manager"
    return "Needs Review - Missing Budget Info"

def generate_proposal(client: str, context: dict, use_case: str) -> str:
    """
    Uses Google Gemini via REST API to generate a tailored sales proposal.
    """
    past_deals = (", ".join(context["past_deals"]) if context.get("past_deals") else "No prior engagements")

    prompt = f"""You are an expert enterprise sales consultant. Generate a professional, 
detailed sales proposal based on the following information.

CLIENT: {client}
INDUSTRY: {context.get('industry', 'N/A')}
BUDGET: {context.get('budget', 'N/A')}
PAST ENGAGEMENTS: {past_deals}

CLIENT REQUIREMENT:
{use_case}

Generate a structured sales proposal with these sections:
1. Executive Summary
2. Client Context & Understanding
3. Proposed Solution
4. Business Value & Expected ROI
5. Implementation Approach
6. Pricing Estimate
7. Next Steps

Make the proposal specific, actionable, and professional. 
Tailor the solution directly to what the client asked for — do NOT use generic content.
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
            # 2. Secondary AI: Free Unauthenticated API (Pollinations) - No Rule Based!
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
            # Absolute worst-case scenario if both APIs are down
            return f"[AI Error: Both Primary and Secondary AI APIs failed. Err: {e}]\n\nFallback Proposal for {client}:\nRequirement: {use_case}\nBudget: {context.get('budget', 'N/A')}\nIndustry: {context.get('industry', 'N/A')}"

def run_agent(client: str, use_case: str) -> dict:
    """Main agent entry point orchestrating data gathering, generation, and approval."""
    context = fetch_crm_data(client)
    proposal = generate_proposal(client, context, use_case)
    approval_status = simulate_approval(proposal)

    return {
        "proposal": proposal,
        "approval_status": approval_status
    }
