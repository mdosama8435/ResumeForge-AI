import streamlit as st
from frontend.api_client import APIClient
from frontend.components.ui import load_css, render_header, render_badges
from frontend.components.sidebar import render_sidebar

st.set_page_config(page_title="Upload | ResumeForge AI", page_icon="📄", layout="wide")
load_css()
render_sidebar()

render_header("Upload Documents", "Provide your current resume and target job description to begin.", "📄")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div style="margin-bottom: 1rem;">
            <h3 style="display: flex; align-items: center; gap: 10px; margin: 0; color: var(--text-color);"><span style="font-size: 1.5rem;">👤</span> 1. Your Resume</h3>
            <p style="color: var(--text-muted); font-size: 0.9rem; margin-top: 4px;">Upload your latest resume. We support PDF, DOCX, and TXT formats up to 10MB.</p>
        </div>
        """, unsafe_allow_html=True
    )
    resume_file = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt"], key="resume_upload", label_visibility="collapsed")
    
    if resume_file:
        with st.spinner("Parsing semantics..."):
            try:
                res = APIClient.upload_resume(resume_file)
                st.session_state.resume_data = res.get("data", {})
                st.markdown(
                    f"""
                    <div class="premium-card" style="padding: 16px; margin-top: 16px; border-left: 4px solid var(--success); background-color: rgba(34, 197, 94, 0.05);">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div style="display: flex; align-items: center; gap: 12px;">
                                <div style="font-size: 2rem;">📄</div>
                                <div>
                                    <div style="font-weight: 700; color: var(--text-color);">{resume_file.name}</div>
                                    <div style="font-size: 0.8rem; color: var(--text-muted);">{round(resume_file.size / 1024, 2)} KB</div>
                                </div>
                            </div>
                            <span class="badge badge-success">Processed</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True
                )
            except Exception as e:
                st.error(f"Failed to process resume: {e}")

with col2:
    st.markdown(
        """
        <div style="margin-bottom: 1rem;">
            <h3 style="display: flex; align-items: center; gap: 10px; margin: 0; color: var(--text-color);"><span style="font-size: 1.5rem;">🏢</span> 2. Job Description</h3>
            <p style="color: var(--text-muted); font-size: 0.9rem; margin-top: 4px;">Upload the target job description to establish semantic context.</p>
        </div>
        """, unsafe_allow_html=True
    )
    jd_file = st.file_uploader("Upload JD", type=["pdf", "docx", "txt"], key="jd_upload", label_visibility="collapsed")
    
    if jd_file:
        with st.spinner("Extracting requirements..."):
            try:
                res = APIClient.upload_jd(jd_file)
                st.session_state.jd_data = res.get("data", {})
                st.markdown(
                    f"""
                    <div class="premium-card" style="padding: 16px; margin-top: 16px; border-left: 4px solid var(--success); background-color: rgba(34, 197, 94, 0.05);">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div style="display: flex; align-items: center; gap: 12px;">
                                <div style="font-size: 2rem;">📋</div>
                                <div>
                                    <div style="font-weight: 700; color: var(--text-color);">{jd_file.name}</div>
                                    <div style="font-size: 0.8rem; color: var(--text-muted);">{round(jd_file.size / 1024, 2)} KB</div>
                                </div>
                            </div>
                            <span class="badge badge-success">Processed</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True
                )
            except Exception as e:
                st.error(f"Failed to process JD: {e}")

if st.session_state.get("resume_data") and st.session_state.get("jd_data"):
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color: var(--border-color); margin-bottom: 2rem;'>", unsafe_allow_html=True)
    
    col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
    with col_b2:
        if st.button("🚀 Analyze ATS Match", use_container_width=True):
            st.switch_page("pages/03_ATS_Analysis.py")
