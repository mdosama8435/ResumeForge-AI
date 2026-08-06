import streamlit as st
from frontend.components.theme import load_css, render_header, render_card
from frontend.components.sidebar import render_sidebar
from frontend.api_client import APIClient

st.set_page_config(page_title="Settings | ResumeForge AI", page_icon="⚙", layout="wide")
load_css()
render_sidebar()

render_header("Settings & Information", "Configure your AI preferences and view system status.", "⚙")

status = APIClient.check_health()
is_healthy = bool(status)

status_html = "<span style='color: var(--success); font-weight: 600;'>Online</span>" if is_healthy else "<span style='color: var(--danger); font-weight: 600;'>Offline</span>"

app_info_html = f"""
    <div style="margin-bottom: 0.5rem;"><strong style="color: var(--text-color);">Version:</strong> <code style="color: var(--primary-color);">2.0.0-enterprise</code></div>
    <div style="margin-bottom: 0.5rem;"><strong style="color: var(--text-color);">Backend Status:</strong> {status_html}</div>
    <div style="margin-bottom: 0.5rem;"><strong style="color: var(--text-color);">Active AI Model:</strong> <code style="color: var(--primary-color);">Gemini 1.5 Pro</code></div>
    <div style="margin-bottom: 0.5rem;"><strong style="color: var(--text-color);">LangChain Parser:</strong> <code style="color: var(--primary-color);">v0.2.1</code></div>
    <div style="margin-bottom: 0.5rem;"><strong style="color: var(--text-color);">Vector Store:</strong> <code style="color: var(--primary-color);">FAISS (Local)</code></div>
"""

col1, col2 = st.columns(2)

with col1:
    render_card("Application Information", app_info_html, "ℹ️")

with col2:
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0; color: var(--text-color);'>⚙️ Preferences</h3>", unsafe_allow_html=True)
    st.selectbox("Default Theme", ["Premium Light (Default)", "Dark Mode (Beta)"])
    st.slider("AI Creativity (Temperature)", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
    st.markdown("</div>", unsafe_allow_html=True)
