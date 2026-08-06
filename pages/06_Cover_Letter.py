import streamlit as st
from frontend.api_client import APIClient
from frontend.components.theme import load_css, render_header, render_empty_state
from frontend.components.sidebar import render_sidebar

st.set_page_config(page_title="Cover Letter | ResumeForge AI", page_icon="💼", layout="wide")
load_css()
render_sidebar()

render_header("Cover Letter Studio", "Generate and refine a personalized cover letter.", "💼")

if not st.session_state.get("resume_data") or not st.session_state.get("jd_data"):
    render_empty_state("Missing Data", "Please upload both your resume and job description first.", "⚠️")
    st.stop()

if "cover_letter" not in st.session_state:
    html_intro = """
    <div class='premium-card' style='text-align: center; padding: 4rem;'>
        <h3 style='margin-top:0; color: var(--text-color);'>Ready to generate your Cover Letter?</h3>
        <p style='color: var(--text-muted);'>Our AI will analyze your background and the target role to craft a highly persuasive narrative.</p>
    </div>
    """
    st.markdown(html_intro, unsafe_allow_html=True)
    if st.button("✨ Generate AI Cover Letter"):
        with st.spinner("Crafting personalized narrative..."):
            try:
                res = APIClient.generate_cover_letter(st.session_state.jd_data.get("text", ""))
                st.session_state.cover_letter = res.get("data", {}).get("cover_letter", "Error generating cover letter.")
                st.rerun()
            except Exception as e:
                error_msg = str(e)
                if "500 Server Error" in error_msg:
                    st.error("Failed to generate cover letter: The AI provider is currently overloaded or you have hit a rate limit (Quota Exceeded). Please wait a minute and try again.")
                else:
                    st.error(f"Failed to generate cover letter: {error_msg}")
else:
    col_ed, col_pr = st.columns(2)
    
    with col_ed:
        html_ed = "<div class='premium-card' style='height: 600px;'><h4 style='margin-top:0; color: var(--text-color);'>Modern Editor</h4>"
        st.markdown(html_ed, unsafe_allow_html=True)
        edited_cl = st.text_area("Edit Content", st.session_state.cover_letter, height=500, label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_pr:
        html_pr = f"""
        <div class='premium-card' style='height: 600px;'>
            <h4 style='margin-top:0; color: var(--text-color);'>Live Preview</h4>
            <div style='white-space: pre-wrap; font-family: serif; font-size: 1.05rem; padding: 1rem; background: var(--background-color); border: 1px solid var(--border-color); border-radius: 8px; height: 500px; overflow-y: auto; color: var(--text-color);'>{edited_cl}</div>
        </div>
        """
        st.markdown(html_pr, unsafe_allow_html=True)
        
    col_a1, col_a2, col_a3 = st.columns(3)
    with col_a1:
        st.download_button("⬇️ Download Document", data=edited_cl, file_name="Cover_Letter.txt", use_container_width=True)
    with col_a2:
        if st.button("📋 Copy Text", use_container_width=True):
            st.toast("Copied!")
    with col_a3:
        if st.button("🔄 AI Rewrite", use_container_width=True, type="secondary"):
            del st.session_state.cover_letter
            st.rerun()
