import streamlit as st
import requests

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Sales Proposal AI Agent",
    layout="wide"
)

# --------------------------------------------------
# DARK / COPILOT-STYLE UI
# --------------------------------------------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: #e6e6e6;
}
.stButton > button {
    background-color: #1f6feb;
    color: white;
    border-radius: 8px;
    padding: 0.5rem 1.2rem;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# TITLE
# --------------------------------------------------
st.title("Sales Proposal AI Agent")

# --------------------------------------------------
# SIDEBAR INPUTS
# --------------------------------------------------
with st.sidebar:
    st.header("Client Context")

    client = st.text_input("Client Name", value="Acme Corp")

    use_case = st.text_area(
        "Client Requirement",
        value="AI sales proposal for demand forecasting"
    )

# --------------------------------------------------
# RUN AGENT (SESSION_STATE FIX)
# --------------------------------------------------
if st.button("Run Agent"):
    with st.spinner("Agent is reasoning..."):
        try:
            response = requests.post(
                "http://127.0.0.1:8000/run-agent",
                json={
                    "client": client,
                    "use_case": use_case
                },
                timeout=10
            )

            # ✅ STORE RESULT SAFELY
            st.session_state["data"] = response.json()

        except Exception as e:
            st.error("Failed to reach backend")
            st.exception(e)

# --------------------------------------------------
# SHOW AGENT OUTPUT (NO NameError POSSIBLE)
# --------------------------------------------------
if "data" in st.session_state:
    st.subheader("🧾 Generated Proposal")
    st.code(st.session_state["data"]["proposal"])

    st.success(
        f"Approval Status: {st.session_state['data']['approval_status']}"
    )

# --------------------------------------------------
# PDF EXPORT
# --------------------------------------------------
if "data" in st.session_state:
    st.divider()
    st.subheader("📄 Export Proposal")

    if st.button("Download Proposal as PDF"):
        try:
            pdf_response = requests.post(
                "http://127.0.0.1:8000/export-pdf",
                json={
                    "proposal": st.session_state["data"]["proposal"]
                },
                timeout=10
            )

            if pdf_response.status_code == 200:
                st.download_button(
                    label="📥 Click to Download PDF",
                    data=pdf_response.content,
                    file_name="Sales_Proposal.pdf",
                    mime="application/pdf"
                )
            else:
                st.error("Failed to generate PDF")

        except Exception as e:
            st.error("Backend not reachable for PDF export")
            st.exception(e)


# --------------------------------------------------
# AGENT MEMORY VIEWER (ACROSS TIME)
# --------------------------------------------------
st.divider()
st.subheader("🧠 Agent Memory (Across Time)")

if st.checkbox("Show Agent Memory"):
    try:
        mem_response = requests.get(
            f"http://127.0.0.1:8000/memory/{client}",
            timeout=5
        )

        if mem_response.status_code == 200:
            memory_data = mem_response.json()

            past = memory_data.get("past_proposals", [])

            if past:
                for idx, proposal in enumerate(past, start=1):
                    st.markdown(f"**Past Proposal {idx}:**")
                    st.code(proposal)
            else:
                st.info("No past proposals found for this client.")

        else:
            st.error("Failed to fetch agent memory")

    except Exception as e:
        st.error("Backend not reachable for memory lookup")
        st.exception(e)
