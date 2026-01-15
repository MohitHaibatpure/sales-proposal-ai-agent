def simulate_approval(proposal):
    if "budget" in proposal.lower():
        return "Approved by Sales Manager"
    return "Needs Review"
