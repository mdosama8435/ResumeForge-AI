import streamlit as st
from frontend.api_client import APIClient
from frontend.components.theme import load_css, render_header, render_empty_state, build_resume_text
from frontend.components.ui import render_ai_explainability
from frontend.components.sidebar import render_sidebar

st.set_page_config(page_title="Optimizer | ResumeForge AI", page_icon="✨", layout="wide")
load_css()
render_sidebar()

render_header("Resume Optimizer", "AI is dynamically rewriting your resume to perfectly align with the target role.", "✨")

if not st.session_state.get("resume_data") or not st.session_state.get("jd_data"):
    render_empty_state("Missing Data", "Please upload both your resume and job description on the Upload page.", "⚠️")
    st.stop()

jd_text = st.session_state.jd_data.get("text", "Senior Backend Developer")

if "optimized_resume" not in st.session_state:
    with st.spinner("AI is crafting the perfect resume using semantic alignment..."):
        try:
            res = APIClient.optimize_resume(jd_text)
            st.session_state.optimized_resume = res.get("data", {})
        except Exception as e:
            error_msg = str(e)
            if "500 Server Error" in error_msg:
                st.error("Optimization failed: The AI provider is currently overloaded or you have hit a rate limit (Quota Exceeded). Please wait a minute and try again.")
            else:
                st.error(f"Optimization failed: {error_msg}")
            st.stop()

# Simulated structured response for highlighting
original_text = st.session_state.resume_data.get("text", "John Doe\nDeveloper\n\n- Worked on backend caching.\n- Built some APIs.")
optimized_text = build_resume_text(st.session_state.optimized_resume)

st.markdown("<h3 style='margin-bottom: 1rem; color: var(--text-color);'>Side-by-Side Comparison</h3>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    html_1 = f"""
    <div style='background-color: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 12px; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1); overflow: hidden; margin-bottom: 1rem;'>
        <div style='background-color: #F8FAFC; border-bottom: 1px solid #E5E7EB; padding: 16px 24px;'>
            <h4 style='margin:0; color: #111827; font-weight: 700; font-size: 1.1rem;'>Original Resume</h4>
        </div>
        <div style='height: 500px; overflow-y: auto; padding: 24px; background-color: #FFFFFF;'>
            <div style='white-space: pre-wrap; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 0.9rem; color: #4B5563; line-height: 1.6;'>{original_text}</div>
        </div>
    </div>
    """
    st.markdown(html_1, unsafe_allow_html=True)

with col2:
    html_2 = f"""
    <div style='background-color: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 12px; box-shadow: 0 10px 25px -5px rgba(45, 212, 191, 0.2), 0 8px 10px -6px rgba(45, 212, 191, 0.1); overflow: hidden; margin-bottom: 1rem;'>
        <div style='background-color: #F0FDF4; border-bottom: 1px solid #BBF7D0; padding: 16px 24px; display: flex; justify-content: space-between; align-items: center;'>
            <h4 style='margin:0; color: #166534; font-weight: 700; font-size: 1.1rem;'>✨ Optimized Resume</h4>
            <span style='background: #22C55E; color: white; padding: 4px 12px; border-radius: 999px; font-size: 0.75rem; font-weight: 600;'>AI Generated</span>
        </div>
        <div style='height: 500px; overflow-y: auto; padding: 24px; background-color: #FFFFFF;'>
            <div style='white-space: pre-wrap; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 0.9rem; color: #111827; line-height: 1.6;'>{optimized_text}</div>
        </div>
    </div>
    """
    st.markdown(html_2, unsafe_allow_html=True)

st.markdown("<h3 style='margin: 2rem 0 1rem 0; color: var(--text-color);'>AI Explainability Engine</h3>", unsafe_allow_html=True)

explainability_data = st.session_state.optimized_resume.get("explainability", [])

if explainability_data:
    for item in explainability_data:
        render_ai_explainability(
            section=item.get("section", "General"),
            reason=item.get("reason", "Optimization"),
            impact=item.get("impact", "Medium"),
            confidence=item.get("confidence", "95%")
        )
else:
    st.info("No explainability data available for this generation.")

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
if st.button("🔄 Regenerate Variations", use_container_width=True):
    del st.session_state.optimized_resume
    st.rerun()
