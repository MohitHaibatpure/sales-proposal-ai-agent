# 🚀 Sales Proposal AI Agent

An enterprise-grade AI Agent that automates end-to-end sales proposal creation. This project was built to demonstrate advanced **Stateless Microservice Architecture**, **High Availability AI Failover**, and **Dynamic Document Generation**.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg?style=for-the-badge&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.25+-FF4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)
![Architecture](https://img.shields.io/badge/Architecture-Stateless-orange.svg?style=for-the-badge)

---

## ⚡ What It Does

- 🎯 **Dynamic Scope Inference:** Takes a simple Sales Client Name & Requirement from the user.
- 🧠 **Generative Synthesis:** Infers an appropriate industry, estimates a realistic budget, and generates a fully tailored Go-To-Market Sales Proposal.
- ⚙️ **Internal Approval Logic:** Parses the generated proposal to determine and simulate managerial business-rule approvals.
- 📄 **Export to Gridded PDF:** Intelligently renders the generated markdown tables and styling into a neat, gridded PDF document via an in-memory byte buffer.

---

## 🏗️ Architecture & Tech Stack

This project was intentionally engineered to follow **Cloud-Native, Stateless** best practices, making it instantly ready to deploy on AWS / Kubernetes environments.

### 🎨 1. Frontend Layer
* **Technology:** **`Streamlit`**
* **Engineering Purpose:** Allows for the rapid prototyping of AI tools with integrated, seamless state management and modern "Copilot" UI styling.

### 🚀 2. API & Backend Orchestration
* **Technology:** **`FastAPI`**
* **Engineering Purpose:** Extends high-performance ASGI execution. Built-in `Pydantic` ensures strict type validation on incoming requests, and custom active CORS middleware enforces secure cross-origin communication.

### 🧠 3. Generative Ecosystem & Failover Routing
* **Technologies:** **`Google Gemini 2.0 Flash`** + **`Pollinations AI`**
* **Engineering Purpose:** 
  * The primary REST interface connects directly to Google Gemini for hyper-fast logical reasoning. 
  * **High Availability Failover:** If Gemini hits a HTTP rate limit, the backend securely intercepts the crash and dynamically re-routes the payload to the secondary Pollinations API, ensuring 100% continuous application uptime.

### 📄 4. Stateless Document Streaming
* **Technology:** **`ReportLab Platypus`**
* **Engineering Purpose:** Employs a custom, intelligent Markdown-to-PDF parser. Bypasses hard drive disk I/O bottlenecks completely by streaming the generated Proposal PDFs directly from system RAM (`io.BytesIO`) securely down to the HTTP client.

---

## 🚀 How to Run Externally

### 1. Initialize the Environment
Ensure you have an API key from Google AI Studio. 
Create an `.env` file in the root directory:

```env
GEMINI_API_KEY=AIzaSy...YourKeyHere...
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the Backend API (FastAPI)

```bash
uvicorn backend.main:app --reload
```
> *The API is now natively exposing endpoints at `http://localhost:8000`*

### 4. Start the Frontend Application

In a **new** terminal:
```bash
streamlit run frontend/app.py
```
> *The Copilot UI is now hosted at `http://localhost:8501`*

---

## 📂 Source Code Layout

A major focus of this project was reducing boilerplate into purely functional code logic. The entire orchestrator relies on exactly three files.

```text
sales-proposal-ai-agent/
├── backend/
│   ├── main.py            # FastAPI REST endpoints + RAM-level Stateless PDF generation
│   └── agent.py           # Core agent logic, LLM Prompting, and Failover routing
├── frontend/
│   └── app.py             # Streamlit Copilot-style interface
├── INTERVIEW_GUIDE.md     # Deep-dive Architecture Documentation
├── requirements.txt       # Dependency tree
└── .env                   # Environment variables (Git-ignored)
```
