# 🚀 Sales Proposal AI Agent — RAG Edition

A **RAG-powered** (Retrieval-Augmented Generation) AI agent that generates professional sales proposals. Built with **LangChain**, **FAISS**, **Google Gemini**, and **Streamlit**.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-Framework-green.svg?style=for-the-badge)
![FAISS](https://img.shields.io/badge/FAISS-Vector_DB-orange.svg?style=for-the-badge)
![Gemini](https://img.shields.io/badge/Gemini_2.0-Flash-red.svg?style=for-the-badge&logo=google&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)

---

## ⚡ What It Does

- 🎯 **Dynamic Scope Inference:** Takes a Client Name & Requirement and generates a tailored sales proposal.
- 📎 **RAG-Enhanced (Optional):** Upload a PDF document — the system extracts, chunks, embeds, and retrieves relevant context to ground the proposal in real data.
- 🧠 **Generative Synthesis:** Uses Google Gemini 2.0 Flash via LangChain to produce a structured 7-section proposal.
- ⚙️ **Approval Simulation:** Automatically determines approval status based on business rules.
- 📄 **PDF Export:** Download the generated proposal as a professionally formatted PDF.

---

## 🏗️ Architecture — RAG Pipeline

```
User Input (Client + Requirement)
        │
        ▼
┌─────────────────────────┐
│   Document Loading      │ ← PyPDFLoader (optional PDF upload)
│   Text Chunking         │ ← RecursiveCharacterTextSplitter
│   Embeddings            │ ← GoogleGenerativeAIEmbeddings
│   FAISS Vector Store    │ ← In-memory vector index
└─────────┬───────────────┘
          │
          ▼
┌─────────────────────────┐
│  Similarity Retrieval   │ ← Top-k nearest chunks
│  + Prompt Augmentation  │
└─────────┬───────────────┘
          │
          ▼
┌─────────────────────────┐
│  Gemini LLM Generation  │ ← ChatGoogleGenerativeAI (Primary)
│  Pollinations Fallback  │ ← Free API (Secondary, if Gemini fails)
│  Approval Simulation    │
│  PDF Export (ReportLab)  │
└─────────────────────────┘
          │
          ▼
     Streamlit UI
```

---

## 📂 Folder Structure

```text
sales-proposal-ai-agent/
├── app.py              # Streamlit frontend (entry point)
├── rag_pipeline.py     # Core RAG pipeline (load, chunk, embed, retrieve, generate)
├── pdf_export.py       # In-memory PDF generation (ReportLab)
├── requirements.txt    # Python dependencies
├── .env                # API key (Git-ignored)
├── .gitignore
└── README.md
```

---

## 🚀 How to Run

### 1. Set Up API Key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=AIzaSy...YourKeyHere...
```

Get your key from [Google AI Studio](https://aistudio.google.com/apikey).

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the App

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501` 🎉

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3.10+** | Core language |
| **LangChain** | AI orchestration framework |
| **FAISS** | Vector similarity search |
| **Google Gemini 2.0 Flash** | Primary LLM + Embeddings |
| **Pollinations AI** | Secondary LLM fallback (free, unauthenticated) |
| **Streamlit** | Web frontend |
| **ReportLab** | PDF generation |
| **python-dotenv** | Secure API key management |
