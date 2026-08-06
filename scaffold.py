import os

structure = {
    "config": ["__init__.py", "logging.py", "settings.py", "constants.py"],
    "exceptions": ["__init__.py", "base.py", "parser_exception.py", "embedding_exception.py", "llm_exception.py", "ats_exception.py", "pdf_exception.py"],
    "utils": ["__init__.py", "helper.py", "file_utils.py", "text_utils.py"],
    "services": ["__init__.py", "parser_service.py", "embedding_service.py", "retriever_service.py", "ats_service.py", "llm_service.py", "resume_service.py", "interview_service.py", "pdf_service.py"],
    "models": ["__init__.py", "resume_model.py", "jd_model.py", "ats_model.py", "response_model.py"],
    "api": {
        "__init__.py": "",
        "routers": ["__init__.py", "upload.py", "analyze.py", "generate.py", "interview.py", "download.py"]
    },
    "frontend": {
        "__init__.py": "",
        "pages": ["__init__.py", "home.py", "dashboard.py", "analyze_resume.py", "ats_report.py", "resume_generator.py", "interview_prep.py", "settings.py"],
        "components": ["__init__.py", "sidebar.py"],
        "assets": ["style.css"]
    },
    "tests": {
        "__init__.py": "",
        "parser": ["__init__.py"],
        "ats": ["__init__.py"],
        "llm": ["__init__.py"],
        "api": ["__init__.py"]
    },
    "docs": ["Architecture.md", "API.md", "Deployment.md", "PromptEngineering.md"],
}

files_content = {
    "requirements.txt": "fastapi\nuvicorn\nstreamlit\nlangchain\nlangchain-google-genai\nsentence-transformers\nfaiss-cpu\nreportlab\nPyMuPDF\npython-docx\npydantic\npydantic-settings\nloguru\nrequests\npython-multipart\n",
    ".env.example": "GEMINI_API_KEY=\nLOG_LEVEL=INFO\nENVIRONMENT=development\n",
    ".gitignore": "venv/\n.idea/\n.vscode/\n.env\n__pycache__/\noutputs/\nuploads/\n*.pyc\n.pytest_cache/\n",
    "Dockerfile": "FROM python:3.12-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\nCOPY . .\nENV PYTHONPATH=/app\nEXPOSE 8000\nCMD [\"uvicorn\", \"main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]\n",
    "docker-compose.yml": "version: '3.8'\nservices:\n  backend:\n    build: .\n    ports:\n      - \"8000:8000\"\n    env_file:\n      - .env\n    volumes:\n      - .:/app\n  frontend:\n    build:\n      context: .\n      dockerfile: Dockerfile.frontend\n    ports:\n      - \"8501:8501\"\n    env_file:\n      - .env\n    volumes:\n      - .:/app\n",
    "Dockerfile.frontend": "FROM python:3.12-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\nCOPY . .\nENV PYTHONPATH=/app\nEXPOSE 8501\nCMD [\"streamlit\", \"run\", \"app.py\", \"--server.port=8501\", \"--server.address=0.0.0.0\"]\n",
    "Makefile": "install:\n\tpip install -r requirements.txt\n\nrun:\n\tuvicorn main:app --reload\n\ntest:\n\tpytest\n\nlint:\n\tflake8 .\n\nformat:\n\tblack .\n\nclean:\n\trm -rf __pycache__ outputs uploads\n",
    "README.md": "# ResumeForge AI\n\n## Project Overview\nAI Powered Resume Tailoring Platform using RAG + Gemini.\n\n## Architecture\nFastAPI backend, Streamlit frontend, LangChain AI core.\n\n## Installation\n`make install`\n\n## Run Instructions\nBackend: `make run`\nFrontend: `streamlit run app.py`\n\n## Folder Structure\nFollows Clean Architecture.\n\n## Future Scope\nOAuth, Payments, multi-model support.\n\n## Contributors\nSenior AI Architect\n",
    "startup.py": "from config.logging import setup_logging\n\ndef init_app():\n    setup_logging()\n    # Additional startup logic (e.g., loading models) goes here\n    pass\n",
    "main.py": "from fastapi import FastAPI\nfrom api.routers import upload, analyze, generate, interview, download\nfrom startup import init_app\n\ninit_app()\n\napp = FastAPI(title=\"ResumeForge AI\")\n\napp.include_router(upload.router, prefix=\"/api\")\napp.include_router(analyze.router, prefix=\"/api\")\napp.include_router(generate.router, prefix=\"/api\")\napp.include_router(interview.router, prefix=\"/api\")\napp.include_router(download.router, prefix=\"/api\")\n\n@app.get(\"/\")\ndef root():\n    return {\"message\": \"ResumeForge AI API\"}\n",
    "app.py": "import streamlit as st\nfrom frontend.components.sidebar import render_sidebar\nfrom frontend.pages import home, dashboard, analyze_resume, ats_report, resume_generator, interview_prep, settings\n\nst.set_page_config(page_title=\"ResumeForge AI\", layout=\"wide\")\n\ndef main():\n    page = render_sidebar()\n    if page == \"Home\":\n        home.render()\n    elif page == \"Dashboard\":\n        dashboard.render()\n    elif page == \"Analyze Resume\":\n        analyze_resume.render()\n    elif page == \"ATS Report\":\n        ats_report.render()\n    elif page == \"Resume Generator\":\n        resume_generator.render()\n    elif page == \"Interview Prep\":\n        interview_prep.render()\n    elif page == \"Settings\":\n        settings.render()\n\nif __name__ == \"__main__\":\n    main()\n",
    "config/logging.py": "import sys\nfrom loguru import logger\nfrom config.settings import settings\n\ndef setup_logging():\n    logger.remove()\n    logger.add(sys.stdout, level=settings.LOG_LEVEL)\n    logger.add(\"app.log\", rotation=\"10 MB\", level=settings.LOG_LEVEL)\n",
    "config/settings.py": "from pydantic_settings import BaseSettings, SettingsConfigDict\n\nclass Settings(BaseSettings):\n    GEMINI_API_KEY: str = \"\"\n    LOG_LEVEL: str = \"INFO\"\n    ENVIRONMENT: str = \"development\"\n    \n    model_config = SettingsConfigDict(env_file=\".env\", env_ignore_empty=True)\n\nsettings = Settings()\n",
    "config/constants.py": "MAX_UPLOAD_SIZE = 5 * 1024 * 1024\nALLOWED_EXTENSIONS = {\".pdf\", \".docx\", \".txt\"}\n",
    "exceptions/base.py": "class ResumeForgeException(Exception):\n    \"\"\"Base exception for ResumeForge AI\"\"\"\n    pass\n",
    "exceptions/parser_exception.py": "from .base import ResumeForgeException\nclass ParserException(ResumeForgeException):\n    pass\n",
    "exceptions/embedding_exception.py": "from .base import ResumeForgeException\nclass EmbeddingException(ResumeForgeException):\n    pass\n",
    "exceptions/llm_exception.py": "from .base import ResumeForgeException\nclass LLMException(ResumeForgeException):\n    pass\n",
    "exceptions/ats_exception.py": "from .base import ResumeForgeException\nclass ATSException(ResumeForgeException):\n    pass\n",
    "exceptions/pdf_exception.py": "from .base import ResumeForgeException\nclass PDFException(ResumeForgeException):\n    pass\n",
    "frontend/assets/style.css": "/* Modern Glassmorphism Theme */\nbody { background: #0f172a; color: #f8fafc; font-family: 'Inter', sans-serif; }\n.stApp { background: linear-gradient(135deg, #1e293b, #0f172a); }\n.glass-panel { background: rgba(255,255,255,0.05); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 1.5rem; }\n",
    "frontend/components/sidebar.py": "import streamlit as st\n\ndef render_sidebar():\n    st.sidebar.title(\"ResumeForge AI\")\n    st.sidebar.markdown(\"---\")\n    return st.sidebar.radio(\"Navigation\", [\"Home\", \"Dashboard\", \"Analyze Resume\", \"ATS Report\", \"Resume Generator\", \"Interview Prep\", \"Settings\"])\n",
    "frontend/pages/home.py": "import streamlit as st\ndef render():\n    st.title(\"Home\")\n    st.write(\"Welcome to ResumeForge AI\")\n",
    "frontend/pages/dashboard.py": "import streamlit as st\ndef render():\n    st.title(\"Dashboard\")\n    st.write(\"Professional Dashboard\")\n",
    "frontend/pages/analyze_resume.py": "import streamlit as st\ndef render():\n    st.title(\"Analyze Resume\")\n    st.write(\"Upload and analyze module (To be implemented)\")\n",
    "frontend/pages/ats_report.py": "import streamlit as st\ndef render():\n    st.title(\"ATS Report\")\n    st.write(\"ATS score and gap analysis (To be implemented)\")\n",
    "frontend/pages/resume_generator.py": "import streamlit as st\ndef render():\n    st.title(\"Resume Generator\")\n    st.write(\"AI Resume generation (To be implemented)\")\n",
    "frontend/pages/interview_prep.py": "import streamlit as st\ndef render():\n    st.title(\"Interview Prep\")\n    st.write(\"Interview questions generator (To be implemented)\")\n",
    "frontend/pages/settings.py": "import streamlit as st\ndef render():\n    st.title(\"Settings\")\n    st.write(\"Application settings (To be implemented)\")\n",
}

def create_structure(base_path, struct):
    for key, value in struct.items():
        if isinstance(value, list):
            os.makedirs(os.path.join(base_path, key), exist_ok=True)
            for item in value:
                with open(os.path.join(base_path, key, item), 'w') as f:
                    if item.endswith('.py') and item != '__init__.py' and os.path.join(key, item).replace('\\', '/') not in files_content:
                        f.write(f'# {item} skeleton\\n')
                    elif item == '__init__.py':
                        f.write('')
        elif isinstance(value, dict):
            os.makedirs(os.path.join(base_path, key), exist_ok=True)
            create_structure(os.path.join(base_path, key), value)

create_structure('.', structure)

for filepath, content in files_content.items():
    os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# Add boilerplate to api routers
routers = ["upload", "analyze", "generate", "interview", "download"]
for router in routers:
    with open(f"api/routers/{router}.py", "w") as f:
        f.write(f"from fastapi import APIRouter\\n\\nrouter = APIRouter(tags=['{router}'])\\n\\n@{router}.post('/{router}')\\ndef {router}_endpoint():\\n    pass\\n")

# Add boilerplate to models
models = ["resume_model", "jd_model", "ats_model", "response_model"]
for model in models:
    class_name = "".join(word.capitalize() for word in model.split('_'))
    with open(f"models/{model}.py", "w") as f:
        f.write(f"from pydantic import BaseModel\\n\\nclass {class_name}(BaseModel):\\n    pass\\n")

print("Scaffolding complete.")
