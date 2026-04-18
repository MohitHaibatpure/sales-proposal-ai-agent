import streamlit as st
import requests

BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Sales Proposal AI Agent",
    layout="wide"
)

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

st.title("Sales Proposal AI Agent")

with st.sidebar:
    st.header("Client Context")

    client = st.text_input("Client Name")

    use_case = st.text_area(
        "Client Requirement"
    )

if st.button("Run Agent"):
    with st.spinner("Agent is reasoning..."):
        try:
            response = requests.post(
                f"{BASE_URL}/run-agent",
                json={
                    "client": client,
                    "use_case": use_case
                },
                timeout=60
            )

            st.session_state["data"] = response.json()

        except Exception as e:
            st.error("Failed to reach backend. Is the FastAPI server running?")
            st.exception(e)

# --------------------------------------------------
# SHOW AGENT OUTPUT
# --------------------------------------------------
if "data" in st.session_state:
    st.subheader("🧾 Generated Proposal")
    st.code(st.session_state["data"]["proposal"])

    st.success(
        f"Approval Status: {st.session_state['data']['approval_status']}"
    )

# --------------------------------------------------
# PDF EXPORT (simplified — single click)
# --------------------------------------------------
if "data" in st.session_state:
    st.divider()
    st.subheader("📄 Export Proposal")

    # Fetch PDF immediately and show download button
    try:
        pdf_response = requests.post(
            f"{BASE_URL}/export-pdf",
            json={
                "proposal": st.session_state["data"]["proposal"]
            },
            timeout=10
        )

        if pdf_response.status_code == 200:
            st.download_button(
                label="📥 Download Proposal as PDF",
                data=pdf_response.content,
                file_name="Sales_Proposal.pdf",
                mime="application/pdf"
            )
        else:
            st.error("Failed to generate PDF")

    except Exception:
        st.warning("PDF export unavailable — backend not reachable")


