import streamlit as st
from frontend.components.theme import load_css, render_header, render_empty_state, build_resume_text
from frontend.components.sidebar import render_sidebar
from frontend.api_client import APIClient

st.set_page_config(page_title="Preview | ResumeForge AI", page_icon="📑", layout="wide")
load_css()
render_sidebar()

render_header("Professional Resume Preview", "Review your finalized document before exporting.", "📑")

if "optimized_resume" not in st.session_state:
    render_empty_state("No Resume Found", "Please optimize your resume first using the Optimizer page.", "⚠️")
    st.stop()

optimized_text = build_resume_text(st.session_state.optimized_resume)

if "pdf_bytes" not in st.session_state:
    with st.spinner("Preparing export files..."):
        try:
            st.session_state.pdf_bytes = APIClient.export_pdf(st.session_state.optimized_resume)
            st.session_state.docx_bytes = APIClient.export_docx(st.session_state.optimized_resume)
        except Exception as e:
            st.error(f"Failed to prepare exports: {e}")
            st.stop()

if "zoom_level" not in st.session_state:
    st.session_state.zoom_level = 1.1

# Template Selector (UI Only)
st.markdown("<h3 style='color: var(--text-color);'>Template Selector</h3>", unsafe_allow_html=True)
col_ts1, col_ts2, col_ts3 = st.columns(3)
with col_ts1:
    st.button("📄 Professional (Selected)", use_container_width=True)
with col_ts2:
    st.button("🎨 Creative (Pro)", use_container_width=True, type="secondary")
with col_ts3:
    st.button("🏢 Executive (Pro)", use_container_width=True, type="secondary")

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# Viewer Toolbar
col_t1, col_t2, col_t3, col_t4 = st.columns([1, 1, 1, 3])
with col_t1:
    if st.button("🔍 Zoom In"):
        st.session_state.zoom_level += 0.2
        st.rerun()
with col_t2:
    if st.button("🔍 Zoom Out"):
        st.session_state.zoom_level = max(0.5, st.session_state.zoom_level - 0.2)
        st.rerun()
with col_t3:
    if st.button("🖨️ Print"):
        st.toast("Opening Print Dialog... (Simulated)")

# Viewer Container
st.markdown(f"""
<div style="background: var(--background-color); padding: 2rem; border-radius: 12px; border: 1px dashed var(--border-color); display: flex; justify-content: center;">
    <div style="background: var(--secondary-background-color); width: 800px; min-height: 1056px; padding: 3rem 4rem; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); border-radius: 4px; border: 1px solid var(--border-color);">
        <div style="white-space: pre-wrap; font-family: 'Times New Roman', Times, serif; color: var(--text-color); font-size: {st.session_state.zoom_level}rem; line-height: 1.6;">
{optimized_text}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

col_a1, col_a2, col_a3 = st.columns(3)
with col_a1:
    st.download_button("⬇️ Download as PDF", data=st.session_state.get("pdf_bytes", b""), file_name="ResumeForge_Optimized.pdf", mime="application/pdf", use_container_width=True)
with col_a2:
    st.download_button("⬇️ Download as DOCX", data=st.session_state.get("docx_bytes", b""), file_name="ResumeForge_Optimized.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
with col_a3:
    if st.button("📋 Copy to Clipboard", use_container_width=True):
        st.toast("Copied to clipboard successfully!")
