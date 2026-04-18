import os
import tempfile
import requests
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate

load_dotenv(override=True)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.7,
    convert_system_message_to_human=True,
)

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=GEMINI_API_KEY,
)

def load_and_chunk_pdf(uploaded_file) -> list:

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    loader = PyPDFLoader(tmp_path)
    pages = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = text_splitter.split_documents(pages)

    os.unlink(tmp_path)
    return chunks

def build_vector_store(chunks: list) -> FAISS:
    vector_store = FAISS.from_documents(chunks, embeddings)
    return vector_store

def retrieve_context(vector_store: FAISS, query: str, k: int = 4) -> list:
    results = vector_store.similarity_search(query, k=k)
    return results

PROPOSAL_PROMPT_WITHOUT_CONTEXT = """You are an expert enterprise sales consultant. Generate a highly professional, detailed sales proposal for the following deal:

CLIENT: {client}
CLIENT REQUIREMENT:
{use_case}

Based strictly on this requirement, intelligently infer the industry and scale of the project.
You MUST format your response EXACTLY following this structure, using identical headings, bullet points, and markdown tables. Do NOT deviate from this layout.

# Sales Proposal

{client}
Proposal for a [Insert specific inferred Solution Name]
*Prepared by: [Your Consulting Firm]*
*Date: [Insert Today's Date]*

---

## 1. Executive Summary
[Provide a strong 4-5 sentence executive summary outlining the core problem and proposed solution.]

---

## 2. Client Context & Understanding
- **Mission:** [State the inferred mission]
- **Stakeholders:** [List key stakeholders]
- **Key Pain Points:**
1. [Pain Point 1]
2. [Pain Point 2]
3. [Pain Point 3]

[Provide a short paragraph summarizing how the solution addresses these pain points]

---

## 3. Proposed Solution
| Component | Description | How it Satisfies Client Needs |
|---|---|---|
| [Component 1] | [Description] | [Satisfaction] |
| [Component 2] | [Description] | [Satisfaction] |
| [Component 3] | [Description] | [Satisfaction] |

---

## 4. Business Value & Expected ROI
| Metric | Projected Impact (Year 1) |
|---|---|
| [Metric 1] | [Impact] |
| [Metric 2] | [Impact] |
| [Metric 3] | [Impact] |

**ROI Calculation:**
- **Capital outlay:** [Estimated Cost]
- **Operational savings:** [Estimated Savings]
- **Net benefit:** [Calculate Net Benefit], yielding a [Percentage] ROI in Year 1.

---

## 5. Implementation Approach
| Phase | Duration | Deliverables |
|---|---|---|
| Discovery & Design | [Time] | [Deliverables] |
| Core Development | [Time] | [Deliverables] |
| Pilot & Validation | [Time] | [Deliverables] |
| Rollout & Training | [Time] | [Deliverables] |
| Post-Go-Live Support | [Time] | [Deliverables] |

A dedicated **Project Success Manager** will coordinate weekly touchpoints, ensuring transparency and capturing iterative stakeholder feedback.

---

## 6. Pricing Estimate
| Item | Cost (USD) |
|---|---|
| Platform Development (incl. infrastructure, etc) | [Cost] |
| Pilot Deployment & Support | [Cost] |
| Training & Change Management | [Cost] |
| **Total Estimated Cost** | **[Total Cost]** |

*Payment terms:* 30% upfront, 40% upon pilot completion, 30% post-go-live. Future enhancements will be scoped separately.

---

## 7. Next Steps
1. **Kickoff Call** - Align on success criteria and refine project scope.
2. **Signed NDA & Engagement Letter** - Formalize partnership.
3. **Discovery Workshop** - Capture detailed workflows and KPI definitions.
4. **Sign-off on Blueprint** - Approve UI/UX mockups and data models.
5. **Commence Development** - Begin Sprint 0, followed by iterative delivery.

We look forward to partnering with {client} to deliver outstanding results.

*Prepared by:* **[Your Name] - Senior Enterprise Solutions Consultant**  
*Signature:* ______________________  
*Date:* ________________________

Make the proposal specific, actionable, and highly professional. Tailor the content directly to what the client asked for. Keep the total length around 500-600 words."""

PROPOSAL_PROMPT_WITH_CONTEXT = """You are an expert enterprise sales consultant. Generate a highly professional, detailed sales proposal for the following deal:

CLIENT: {client}
CLIENT REQUIREMENT:
{use_case}

RELEVANT DOCUMENT CONTEXT (from uploaded PDF):
{context}

Using the above document context along with the requirement, intelligently infer the industry and scale of the project. Ground your proposal in the specifics from the uploaded document.
You MUST format your response EXACTLY following this structure, using identical headings, bullet points, and markdown tables. Do NOT deviate from this layout.

# Sales Proposal

{client}
Proposal for a [Insert specific inferred Solution Name]
*Prepared by: [Your Consulting Firm]*
*Date: [Insert Today's Date]*

---

## 1. Executive Summary
[Provide a strong 4-5 sentence executive summary outlining the core problem and proposed solution.]

---

## 2. Client Context & Understanding
- **Mission:** [State the inferred mission]
- **Stakeholders:** [List key stakeholders]
- **Key Pain Points:**
1. [Pain Point 1]
2. [Pain Point 2]
3. [Pain Point 3]

[Provide a short paragraph summarizing how the solution addresses these pain points]

---

## 3. Proposed Solution
| Component | Description | How it Satisfies Client Needs |
|---|---|---|
| [Component 1] | [Description] | [Satisfaction] |
| [Component 2] | [Description] | [Satisfaction] |
| [Component 3] | [Description] | [Satisfaction] |

---

## 4. Business Value & Expected ROI
| Metric | Projected Impact (Year 1) |
|---|---|
| [Metric 1] | [Impact] |
| [Metric 2] | [Impact] |
| [Metric 3] | [Impact] |

**ROI Calculation:**
- **Capital outlay:** [Estimated Cost]
- **Operational savings:** [Estimated Savings]
- **Net benefit:** [Calculate Net Benefit], yielding a [Percentage] ROI in Year 1.

---

## 5. Implementation Approach
| Phase | Duration | Deliverables |
|---|---|---|
| Discovery & Design | [Time] | [Deliverables] |
| Core Development | [Time] | [Deliverables] |
| Pilot & Validation | [Time] | [Deliverables] |
| Rollout & Training | [Time] | [Deliverables] |
| Post-Go-Live Support | [Time] | [Deliverables] |

A dedicated **Project Success Manager** will coordinate weekly touchpoints, ensuring transparency and capturing iterative stakeholder feedback.

---

## 6. Pricing Estimate
| Item | Cost (USD) |
|---|---|
| Platform Development (incl. infrastructure, etc) | [Cost] |
| Pilot Deployment & Support | [Cost] |
| Training & Change Management | [Cost] |
| **Total Estimated Cost** | **[Total Cost]** |

*Payment terms:* 30% upfront, 40% upon pilot completion, 30% post-go-live. Future enhancements will be scoped separately.

---

## 7. Next Steps
1. **Kickoff Call** - Align on success criteria and refine project scope.
2. **Signed NDA & Engagement Letter** - Formalize partnership.
3. **Discovery Workshop** - Capture detailed workflows and KPI definitions.
4. **Sign-off on Blueprint** - Approve UI/UX mockups and data models.
5. **Commence Development** - Begin Sprint 0, followed by iterative delivery.

We look forward to partnering with {client} to deliver outstanding results.

*Prepared by:* **[Your Name] - Senior Enterprise Solutions Consultant**  
*Signature:* ______________________  
*Date:* ________________________

Make the proposal specific, actionable, and highly professional. Tailor the content directly to what the client asked for. Keep the total length around 500-600 words."""

def _build_raw_prompt(client: str, use_case: str, context: str = None) -> str:
    if context:
        return PROPOSAL_PROMPT_WITH_CONTEXT.format(
            client=client, use_case=use_case, context=context
        )
    return PROPOSAL_PROMPT_WITHOUT_CONTEXT.format(
        client=client, use_case=use_case
    )

def _call_pollinations_fallback(prompt: str) -> str:
    fallback_url = "https://text.pollinations.ai/"
    fallback_payload = {
        "messages": [
            {"role": "system", "content": "You are an expert sales proposal generator. Output ONLY the proposal text with clean markdown formatting. Do not include any JSON, metadata, or reasoning."},
            {"role": "user", "content": prompt},
        ],
        "model": "openai",
    }
    response = requests.post(fallback_url, json=fallback_payload, timeout=60)
    response.raise_for_status()

    raw = response.text.strip()
    try:
        data = response.json()
        if isinstance(data, dict) and "choices" in data:
            return data["choices"][0]["message"]["content"].strip()
        if isinstance(data, dict) and "content" in data:
            return data["content"].strip()
        if isinstance(data, list) and len(data) > 0:
            return data[0].get("content", raw).strip()
    except (ValueError, KeyError, IndexError):
        pass

    return raw


def generate_proposal(client: str, use_case: str, vector_store: FAISS = None) -> str:
    context_text = None
    if vector_store:
        relevant_docs = retrieve_context(vector_store, use_case, k=4)
        context_text = "\n\n".join([doc.page_content for doc in relevant_docs])

    try:
        if context_text:
            prompt = ChatPromptTemplate.from_template(PROPOSAL_PROMPT_WITH_CONTEXT)
            chain = prompt | llm
            response = chain.invoke({
                "client": client,
                "use_case": use_case,
                "context": context_text,
            })
        else:
            prompt = ChatPromptTemplate.from_template(PROPOSAL_PROMPT_WITHOUT_CONTEXT)
            chain = prompt | llm
            response = chain.invoke({
                "client": client,
                "use_case": use_case,
            })

        return response.content.strip()

    except Exception as gemini_err:
        try:
            print(f"Gemini failed ({gemini_err}). Switching to Pollinations fallback...")
            raw_prompt = _build_raw_prompt(client, use_case, context_text)
            return _call_pollinations_fallback(raw_prompt)

        except Exception as fallback_err:
            return (
                f"[AI Error: Both Primary (Gemini) and Secondary (Pollinations) AI failed. "
                f"Error: {fallback_err}]\n\n"
                f"Fallback Proposal for {client}:\n"
                f"Requirement: {use_case}\n"
                f"(Due to system failure, we could not generate the AI content)"
            )


def simulate_approval(proposal: str) -> str:
    if "budget" in proposal.lower() or "pricing" in proposal.lower():
        return "Approved by Sales Manager"
    return "Needs Review - Missing Budget Info"

def run_agent(client: str, use_case: str, vector_store: FAISS = None) -> dict:
    proposal = generate_proposal(client, use_case, vector_store)
    approval_status = simulate_approval(proposal)

    return {
        "proposal": proposal,
        "approval_status": approval_status,
    }
