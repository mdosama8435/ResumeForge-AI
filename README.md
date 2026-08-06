# ResumeForge AI ✨

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-00a393.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B.svg)
![LangChain](https://img.shields.io/badge/LangChain-Enabled-lightgrey)

**ResumeForge AI** is an enterprise-grade resume tailoring platform that helps job seekers land more interviews. By leveraging advanced Semantic Matching (RAG + FAISS) and the powerful Gemini AI model, ResumeForge analyzes job descriptions and deterministically optimizes your resume to maximize your ATS (Applicant Tracking System) score.

---

## 🚀 Features

- **Deep ATS Analysis**: Our proprietary parser evaluates your resume against target Job Descriptions, providing a deterministic match score and highlighting critical skill gaps.
- **AI Resume Optimization**: Contextually rewrites your experience bullet points to seamlessly weave in missing keywords without hallucinating facts.
- **Cover Letter Generation**: Automatically crafts bespoke, highly persuasive cover letters customized for the specific role.
- **Interview Prep**: Generates personalized behavioral and technical interview questions based on your background.
- **Professional Exports**: Export your optimized application materials as perfectly formatted PDF or DOCX files.

---

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Backend API**: FastAPI, Uvicorn
- **AI / LLM Orchestration**: LangChain, Google Gemini API (`gemini-flash-latest`)
- **Vector Database (RAG)**: FAISS, Sentence Transformers
- **Document Parsing**: PyMuPDF, python-docx

---

## ⚙️ Local Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/ResumeForge_AI.git
cd ResumeForge_AI
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables
Create a `.env` file in the root directory (you can copy from `.env.example`) and add your Gemini API keys:
```env
# Supports single key or comma-separated for automatic load-balancing/fallback
GEMINI_API_KEY=your_api_key_1,your_api_key_2
LLM_MODEL=gemini-flash-latest
```

---

## 🚦 Running the Application

This architecture separates the Backend (FastAPI) and Frontend (Streamlit) into two different processes.

**Start the Backend Engine:**
```bash
python main.py
# The API will be available at http://localhost:8000
```

**Start the Streamlit Frontend (in a new terminal):**
```bash
streamlit run app.py
# The UI will open automatically in your browser at http://localhost:8501
```

---

## 📜 License
Built for the Future of Work. © 2026 ResumeForge AI.
