import re
import streamlit as st
from rag_pipeline import run_agent, load_and_chunk_pdf, build_vector_store
from pdf_export import create_pdf


def _markdown_to_html(text: str) -> str:
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    # Headings (### before ## before #)
    text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.+)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)

    # Horizontal Rules
    text = re.sub(r'^---$', r'<hr>', text, flags=re.MULTILINE)

    # Bold and italic
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)

    # Numbered section headers (e.g., "1. Executive Summary")
    text = re.sub(
        r'^(\d+)\.\s+(.+)$',
        r'<h3>\1. \2</h3>',
        text,
        flags=re.MULTILINE,
    )

    # Bullet points
    text = re.sub(r'^\s*[-\u2022]\s+(.+)$', r'<li>\1</li>', text, flags=re.MULTILINE)
    text = re.sub(r'((?:<li>.*?</li>\n?)+)', r'<ul>\1</ul>', text)

    # Markdown tables to HTML tables
    lines = text.split('\n')
    result = []
    in_table = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('|') and stripped.endswith('|'):
            if re.match(r'^\|[\s\-:|]+\|$', stripped):
                continue
            cells = [c.strip() for c in stripped.split('|')[1:-1]]
            if not in_table:
                in_table = True
                result.append('<table>')
                result.append('<tr>' + ''.join(f'<th>{c}</th>' for c in cells) + '</tr>')
            else:
                result.append('<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>')
        else:
            if in_table:
                result.append('</table>')
                in_table = False
            result.append(line)
    if in_table:
        result.append('</table>')
    text = '\n'.join(result)

    # Paragraph breaks
    text = re.sub(r'\n\n+', '</p><p>', text)
    text = re.sub(r'(?<!</p>)\n(?!<)', '<br>', text)

    return f'<p>{text}</p>'

st.set_page_config(
    page_title="Sales Proposal AI Agent",
    page_icon="🚀",
    layout="wide",
)

st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Global dark theme */
    .stApp {
        background: linear-gradient(135deg, #0d1117 0%, #161b22 50%, #0d1117 100%);
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #161b22 0%, #0d1117 100%);
        border-right: 1px solid rgba(48, 54, 61, 0.6);
    }

    /* Primary button */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #238636 0%, #2ea043 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.7rem 1.5rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 14px rgba(35, 134, 54, 0.3);
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(35, 134, 54, 0.45);
    }

    /* Secondary buttons */
    .stButton > button {
        background-color: #21262d;
        color: #c9d1d9;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 0.5rem 1.2rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #30363d;
        border-color: #8b949e;
    }

    /* Proposal container */
    .proposal-container {
        background: linear-gradient(135deg, #161b22 0%, #1c2128 100%);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 2rem 2.5rem;
        margin: 1rem 0;
        line-height: 1.8;
        color: #e6edf3;
        font-size: 0.95rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    .proposal-container h1, .proposal-container h2, .proposal-container h3 {
        color: #58a6ff;
        border-bottom: 1px solid #21262d;
        padding-bottom: 0.4rem;
        margin-top: 1.5rem;
    }
    .proposal-container strong, .proposal-container b {
        color: #f0f6fc;
    }
    .proposal-container ul, .proposal-container ol {
        padding-left: 1.5rem;
    }
    .proposal-container li {
        margin-bottom: 0.4rem;
    }
    .proposal-container table {
        width: 100%;
        border-collapse: collapse;
        margin: 1rem 0;
    }
    .proposal-container th, .proposal-container td {
        border: 1px solid #30363d;
        padding: 0.6rem 1rem;
        text-align: left;
    }
    .proposal-container th {
        background-color: #21262d;
        color: #58a6ff;
        font-weight: 600;
    }

    /* Status badges */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.6rem 1.2rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.95rem;
        margin: 0.5rem 0;
    }
    .status-approved {
        background: rgba(35, 134, 54, 0.15);
        border: 1px solid rgba(35, 134, 54, 0.4);
        color: #3fb950;
    }
    .status-review {
        background: rgba(210, 153, 34, 0.15);
        border: 1px solid rgba(210, 153, 34, 0.4);
        color: #d29922;
    }

    /* Section headers */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        color: #e6edf3;
        font-size: 1.3rem;
        font-weight: 700;
        margin: 1.5rem 0 0.8rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #21262d;
    }

    /* Info cards in sidebar */
    .info-card {
        background: rgba(56, 139, 253, 0.1);
        border: 1px solid rgba(56, 139, 253, 0.3);
        border-radius: 8px;
        padding: 0.8rem 1rem;
        margin: 0.5rem 0;
        font-size: 0.85rem;
        color: #8b949e;
    }

    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #1f6feb 0%, #388bfd 100%);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 0.7rem 1.5rem;
        box-shadow: 0 4px 14px rgba(31, 111, 235, 0.3);
        transition: all 0.3s ease;
    }
    .stDownloadButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(31, 111, 235, 0.45);
    }

    /* Alerts */
    .stAlert {
        border-radius: 10px;
    }

    /* Dividers */
    hr {
        border-color: #21262d;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("📋 Client Context")

    client = st.text_input("Client Name")

    use_case = st.text_area("Client Requirement", height=150)

    st.divider()

    st.subheader("📎 Upload Document (Optional)")
    st.caption("Upload a PDF to ground the proposal in your document's context using RAG.")

    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
        label_visibility="collapsed",
    )

    # Process uploaded PDF into vector store
    if uploaded_file is not None:
        if ("uploaded_file_name" not in st.session_state
                or st.session_state.uploaded_file_name != uploaded_file.name):
            with st.spinner("📄 Processing PDF..."):
                chunks = load_and_chunk_pdf(uploaded_file)
                st.session_state.vector_store = build_vector_store(chunks)
                st.session_state.uploaded_file_name = uploaded_file.name
                st.session_state.chunk_count = len(chunks)

        st.success(
            f"✅ **{st.session_state.uploaded_file_name}** loaded\n\n"
            f"📊 {st.session_state.chunk_count} chunks indexed in FAISS"
        )

    st.divider()

    if st.button("🔄 Clear / Reset", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

st.title("🚀 Sales Proposal AI Agent")
st.caption("RAG-powered proposal generation using LangChain + FAISS + Google Gemini")

if st.button("⚡ Generate Proposal", type="primary", use_container_width=True):
    if not client or not use_case:
        st.warning("⚠️ Please enter both a Client Name and a Requirement.")
    else:
        with st.spinner("🧠 Agent is reasoning..."):
            vector_store = st.session_state.get("vector_store", None)
            result = run_agent(client, use_case, vector_store)
            st.session_state["data"] = result

if "data" in st.session_state:
    data = st.session_state["data"]

    # ── Approval Status Badge ──
    status = data["approval_status"]
    if "Approved" in status:
        st.markdown(
            f'<div class="status-badge status-approved">✅ {status}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="status-badge status-review">⏳ {status}</div>',
            unsafe_allow_html=True,
        )

    # ── Generated Proposal (rich container) ──
    st.markdown('<div class="section-header">🧾 Generated Proposal</div>', unsafe_allow_html=True)

    proposal_text = data["proposal"]

    # Render inside a styled container
    st.markdown(
        f'<div class="proposal-container">{_markdown_to_html(proposal_text)}</div>',
        unsafe_allow_html=True,
    )

    # ── PDF Export ──
    st.markdown('<div class="section-header">📄 Export Proposal</div>', unsafe_allow_html=True)

    pdf_bytes = create_pdf(proposal_text)
    st.download_button(
        label="📥 Download Proposal as PDF",
        data=pdf_bytes,
        file_name="Sales_Proposal.pdf",
        mime="application/pdf",
        use_container_width=True,
    )


