import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.set_page_config(page_title="ResumeForge AI | Dashboard", page_icon="✨", layout="wide", initial_sidebar_state="expanded")

from frontend.components.theme import load_css, render_hero_banner, render_card
from frontend.components.sidebar import render_sidebar

load_css()
render_sidebar()

# Hero Section
render_hero_banner(
    title="ResumeForge AI",
    subtitle="Powered by LangChain + Gemini",
    description="Land More Interviews with AI. The most advanced enterprise resume tailoring platform with deterministic ATS scoring and intelligent semantic matching."
)

st.markdown("<div style='text-align: center; margin-bottom: 3rem;'>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col2:
    if st.button("🚀 Start Optimizing Now", use_container_width=True):
        st.switch_page("pages/02_Upload.py")
with col3:
    if st.button("View ATS Analytics", use_container_width=True, type="secondary"):
        st.switch_page("pages/03_ATS_Analysis.py")
st.markdown("</div>", unsafe_allow_html=True)

# Technology Ribbon
st.markdown(
    """
    <div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-bottom: 4rem;">
        <span class="badge badge-primary">LangChain</span>
        <span class="badge badge-primary">Gemini</span>
        <span class="badge badge-primary">FastAPI</span>
        <span class="badge badge-primary">FAISS</span>
        <span class="badge badge-primary">RAG</span>
        <span class="badge badge-primary">Streamlit</span>
        <span class="badge badge-primary">Pydantic</span>
    </div>
    """, unsafe_allow_html=True
)

# KPI Section
col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
with col_kpi1:
    render_card("ATS Accuracy", "<div style='font-size: 3rem; font-weight: 800; color: var(--success); line-height: 1;'>98.4%</div><div style='color: var(--text-muted); font-size: 0.85rem; margin-top: 8px;'>Deterministic parsing algorithms</div>", "🎯")
with col_kpi2:
    render_card("Resumes Optimized", "<div style='font-size: 3rem; font-weight: 800; color: var(--primary-color); line-height: 1;'>12,450</div><div style='color: var(--text-muted); font-size: 0.85rem; margin-top: 8px;'>Across 45+ industries</div>", "📈")
with col_kpi3:
    render_card("Avg Processing Time", "<div style='font-size: 3rem; font-weight: 800; color: var(--accent-color); line-height: 1;'>1.2s</div><div style='color: var(--text-muted); font-size: 0.85rem; margin-top: 8px;'>Lightning fast AI generation</div>", "⚡")

st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

# Feature Grid
st.markdown("<h2 style='text-align: center; margin-bottom: 2rem; color: var(--text-color);'>Enterprise-Grade Features</h2>", unsafe_allow_html=True)

col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    render_card("AI Resume Optimization", "Advanced semantic matching rewrites your bullet points to perfectly align with target job descriptions while retaining absolute truthfulness.", "✨")
    render_card("Interview Preparation", "Generates custom behavioral and technical interview questions based precisely on the gaps found in your resume.", "🎯")

with col_f2:
    render_card("Deep ATS Analysis", "Our proprietary parser mimics modern Applicant Tracking Systems to provide you with a deterministic score and actionable insights.", "📊")
    render_card("Professional PDF Export", "Pixel-perfect formatting ensuring your finalized resume passes through both machine parsers and human recruiters.", "📄")

with col_f3:
    render_card("Semantic Matching", "FAISS vector databases understand the contextual meaning of your experience, going far beyond simple keyword stuffing.", "🧠")
    render_card("Cover Letter Generation", "Craft highly persuasive, bespoke cover letters that naturally weave your unique value proposition with company goals.", "💼")

st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: var(--text-muted); font-size: 0.85rem;'>© 2026 ResumeForge AI | Built for the Future of Work</div>", unsafe_allow_html=True)
