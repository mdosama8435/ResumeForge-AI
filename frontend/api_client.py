import requests
import streamlit as st
from typing import Dict, Any

import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

class APIClient:
    @staticmethod
    def _get_session():
        if "session_id" not in st.session_state:
            import uuid
            st.session_state.session_id = str(uuid.uuid4())
        return st.session_state.session_id

    @staticmethod
    def upload_resume(file) -> Dict[str, Any]:
        url = f"{API_BASE_URL}/upload/resume"
        files = {"file": (file.name, file, file.type)}
        data = {"session_id": APIClient._get_session()}
        response = requests.post(url, files=files, data=data)
        response.raise_for_status()
        return response.json()
        
    @staticmethod
    def upload_jd(file) -> Dict[str, Any]:
        url = f"{API_BASE_URL}/upload/job-description"
        files = {"file": (file.name, file, file.type)}
        data = {"session_id": APIClient._get_session()}
        response = requests.post(url, files=files, data=data)
        response.raise_for_status()
        return response.json()
        
    @staticmethod
    def analyze_ats(resume_data, jd_data) -> Dict[str, Any]:
        url = f"{API_BASE_URL}/analyze"
        payload = {"resume_data": resume_data, "jd_data": jd_data}
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def optimize_resume(jd_text: str) -> Dict[str, Any]:
        url = f"{API_BASE_URL}/generate/resume"
        payload = {"session_id": APIClient._get_session(), "jd_text": jd_text}
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def generate_cover_letter(jd_text: str) -> Dict[str, Any]:
        url = f"{API_BASE_URL}/generate/cover-letter"
        payload = {"session_id": APIClient._get_session(), "jd_text": jd_text}
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_interview(jd_text: str) -> Dict[str, Any]:
        url = f"{API_BASE_URL}/generate/interview"
        payload = {"session_id": APIClient._get_session(), "jd_text": jd_text}
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def export_pdf(opt_data: Dict[str, Any]) -> bytes:
        url = f"{API_BASE_URL}/generate/export/pdf"
        response = requests.post(url, json=opt_data)
        response.raise_for_status()
        return response.content

    @staticmethod
    def export_docx(opt_data: Dict[str, Any]) -> bytes:
        url = f"{API_BASE_URL}/generate/export/docx"
        response = requests.post(url, json=opt_data)
        response.raise_for_status()
        return response.content

    @staticmethod
    def check_health() -> Dict[str, Any]:
        try:
            url = f"{API_BASE_URL}/health"
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                return response.json().get("data", {})
        except Exception:
            pass
        return {}
