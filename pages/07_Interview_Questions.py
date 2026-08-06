import streamlit as st
from frontend.api_client import APIClient
from frontend.components.theme import load_css, render_header, render_empty_state
from frontend.components.sidebar import render_sidebar

st.set_page_config(page_title="Interview Prep | ResumeForge AI", page_icon="🎯", layout="wide")
load_css()
render_sidebar()

render_header("Technical & Behavioral Interview Prep", "AI-generated questions targeting the specific gaps between your resume and the JD.", "🎯")

if not st.session_state.get("jd_data"):
    render_empty_state("Context Missing", "Upload a Job Description to generate targeted questions.", "⚠️")
    st.stop()

jd_text = st.session_state.jd_data.get("text", "Senior Backend Developer")

if st.button("✨ Generate Premium Question Bank", use_container_width=True):
    with st.spinner("Analyzing skill gaps and formulating high-impact scenarios..."):
        try:
            res = APIClient.get_interview(jd_text)
            st.session_state.interview_q = res.get("data", {}).get("questions", [])
        except Exception as e:
            error_msg = str(e)
            if "500 Server Error" in error_msg:
                st.error("Generation failed: The AI provider is currently overloaded or you have hit a rate limit (Quota Exceeded). Please wait a minute and try again.")
            else:
                st.error(f"Generation failed: {error_msg}")

if "interview_q" in st.session_state:
    questions = st.session_state.interview_q
    if not questions:
        st.info("No questions generated. Please try again.")
    else:
        html_header = """
        <div class='premium-card' style='padding: 2rem;'>
            <h3 style='margin-top:0; color: var(--text-color);'>Targeted Question Bank</h3>
            <p style='margin-bottom: 2rem; color: var(--text-muted);'>Practice these customized questions designed to test your weakest matching areas.</p>
        """
        st.markdown(html_header, unsafe_allow_html=True)
        
        for i, q in enumerate(questions):
            title = q.get("question", f"Question {i+1}")
            ans = q.get("expected_answer", "No answer provided.")
            diff = q.get("difficulty", "Medium")
            cat = q.get("category", "General")
            time_est = q.get("estimated_time", "5 mins")
                
            with st.expander(f"Q{i+1}: {title}"):
                st.markdown(
                    f"""
                    <div style="display: flex; gap: 10px; margin-bottom: 1rem;">
                        <span class="badge badge-warning">{diff}</span>
                        <span class="badge badge-success">{cat}</span>
                        <span class="badge badge-primary">⏱️ {time_est}</span>
                    </div>
                    """, unsafe_allow_html=True
                )
                
                st.markdown(
                    f"""
                    <div style="background-color: var(--secondary-background-color); border-left: 4px solid var(--success); border-top: 1px solid var(--border-color); border-right: 1px solid var(--border-color); border-bottom: 1px solid var(--border-color); padding: 1rem; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                        <h4 style="margin-top: 0; color: var(--success); font-size: 0.9rem; text-transform: uppercase;">Expected Answer Blueprint</h4>
                        <p style="margin: 0; font-size: 0.95rem; line-height: 1.6; color: var(--text-muted);">{ans}</p>
                    </div>
                    """, unsafe_allow_html=True
                )
        st.markdown("</div>", unsafe_allow_html=True)
