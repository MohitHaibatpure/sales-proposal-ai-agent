from backend.crm_mock import fetch_crm_data
from backend.memory import save_memory, load_memory
from backend.approval_engine import simulate_approval


def generate_proposal(client: str, context: dict, use_case: str) -> str:
    """
    LLM-ready proposal generator.
    This function is intentionally structured so it can later
    be replaced by an OpenAI / Azure OpenAI call in ONE line.
    """

    past_deals = (
        ", ".join(context["past_deals"])
        if context.get("past_deals")
        else "No prior engagements"
    )

    return f"""
Executive Summary:
This proposal outlines how we can help {client} achieve measurable
business impact using advanced AI capabilities.

Client Context:
- Industry: {context.get('industry', 'N/A')}
- Budget: {context.get('budget', 'N/A')}
- Past Engagements: {past_deals}

Client Requirement:
{use_case}

Proposed Solution:
We propose an AI-driven demand forecasting system tailored specifically
to {client}'s operational and strategic needs. The solution will leverage
historical data, predictive modeling, and intelligent automation.

Business Value:
- Improved demand planning accuracy
- Reduced inventory holding costs
- Faster, data-driven decision-making
- Better alignment between sales and operations

Implementation Approach:
- Initial discovery and data assessment
- Model development and validation
- Deployment and user enablement

Next Steps:
- Internal approval
- Stakeholder alignment
- Final proposal sign-off
""".strip()


def run_agent(payload: dict) -> dict:
    """
    Main agent entry point.
    Orchestrates context gathering, proposal generation,
    memory persistence, and approval simulation.
    """

    client = payload.get("client")
    use_case = payload.get("use_case")

    # 1. Gather enterprise context (CRM, past deals, budget, etc.)
    context = fetch_crm_data(client)

    # 2. Load historical memory (agent reasoning across time)
    _ = load_memory(client)

    # 3. Generate proposal (LLM-ready)
    proposal = generate_proposal(
        client=client,
        context=context,
        use_case=use_case
    )

    # 4. Simulate internal approval workflow
    approval_status = simulate_approval(proposal)

    # 5. Persist memory for future runs
    save_memory(client, proposal)

    return {
        "proposal": proposal,
        "approval_status": approval_status
    }
