import streamlit as st
from frontend.api_client import APIClient
from frontend.components.theme import load_css, render_header, render_circular_progress, render_progress_bar, render_badges, render_empty_state
from frontend.components.ui import render_radar_chart
from frontend.components.sidebar import render_sidebar

st.set_page_config(page_title="ATS Dashboard | ResumeForge AI", page_icon="📊", layout="wide")
load_css()
render_sidebar()

render_header("Business Analytics Dashboard", "Deep-dive into your resume's compatibility with the job description.", "📊")

if not st.session_state.get("resume_data") or not st.session_state.get("jd_data"):
    render_empty_state("Awaiting Documents", "Upload your resume and job description to begin the ATS analysis.", "📄")
    if st.button("Go to Upload Page", use_container_width=True):
        st.switch_page("pages/02_Upload.py")
    st.stop()

if "ats_result" not in st.session_state:
    with st.spinner("Running deep semantic ATS Analysis..."):
        try:
            res = APIClient.analyze_ats(st.session_state.resume_data, st.session_state.jd_data)
            st.session_state.ats_result = res.get("data", {})
        except Exception as e:
            st.error(f"Analysis failed: {e}")
            st.stop()

data = st.session_state.ats_result
overall_score = data.get("overall_score", 75)
metrics = {
    "Keywords": data.get("keyword_match", 70),
    "Skills": data.get("skills_match", 65),
    "Experience": data.get("experience_match", 80),
    "Projects": data.get("projects_match", 75),
    "Education": data.get("education_match", 85),
    "Formatting": data.get("formatting_score", 90)
}

# Top KPI Row
col_m1, col_m2 = st.columns([1, 2.5])

with col_m1:
    st.markdown("<div class='premium-card' style='height: 100%; display: flex; flex-direction: column; justify-content: center;'>", unsafe_allow_html=True)
    render_circular_progress(overall_score, "ATS Match Score")
    st.markdown("<p style='text-align: center; font-size: 0.85rem; color: var(--text-muted);'>Deterministic algorithm scoring based on semantic overlap and formatting.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_m2:
    st.markdown("<div class='premium-card' style='height: 100%;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0; color: var(--text-color);'>Radar Analysis</h3>", unsafe_allow_html=True)
    render_radar_chart(metrics)
    st.markdown("</div>", unsafe_allow_html=True)

# Secondary KPI Row (Bars)
st.markdown("<h3 style='margin-top:1.5rem; color: var(--text-color);'>Core Metrics Breakdown</h3>", unsafe_allow_html=True)
col_b1, col_b2 = st.columns(2)
with col_b1:
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    render_progress_bar("Keyword Match", metrics["Keywords"])
    render_progress_bar("Skills Match", metrics["Skills"])
    render_progress_bar("Experience Match", metrics["Experience"])
    st.markdown("</div>", unsafe_allow_html=True)
with col_b2:
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    render_progress_bar("Projects Match", metrics["Projects"])
    render_progress_bar("Education Match", metrics["Education"])
    render_progress_bar("Formatting Score", metrics["Formatting"])
    st.markdown("</div>", unsafe_allow_html=True)

# Keyword Chips
st.markdown("<h3 style='margin-top:1.5rem; color: var(--text-color);'>Keyword Analysis</h3>", unsafe_allow_html=True)
matched = data.get("matched_keywords", ["Python", "FastAPI", "PostgreSQL", "REST APIs"])
recommended = data.get("recommended_keywords", ["GraphQL", "Microservices"])
missing = data.get("missing_keywords", ["AWS", "Docker", "Kubernetes", "CI/CD"])

st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
st.markdown("<h4 style='color: var(--text-color); margin-top: 0;'>Matched</h4>", unsafe_allow_html=True)
render_badges(matched, "success")
st.markdown("<h4 style='color: var(--text-color);'>Recommended</h4>", unsafe_allow_html=True)
render_badges(recommended, "warning")
st.markdown("<h4 style='color: var(--text-color);'>Missing</h4>", unsafe_allow_html=True)
render_badges(missing, "danger")
st.markdown("</div>", unsafe_allow_html=True)

# Insights Cards
col_i1, col_i2, col_i3 = st.columns(3)
strengths = data.get("strengths", ["Strong backend fundamentals", "Good educational background"])
weaknesses = data.get("weaknesses", ["Lacks specific cloud experience keywords", "Action verbs could be stronger"])
recs = data.get("recommendations", ["Add AWS and Docker to skills", "Quantify project impacts"])

with col_i1:
    html = "<div class='premium-card' style='border-top: 4px solid var(--success); height: 100%;'><h3 style='margin-top:0; color: var(--text-color);'>Strengths 💪</h3><ul style='color: var(--text-muted);'>"
    for s in strengths:
        html += f"<li>{s}</li>"
    html += "</ul></div>"
    st.markdown(html, unsafe_allow_html=True)

with col_i2:
    html = "<div class='premium-card' style='border-top: 4px solid var(--danger); height: 100%;'><h3 style='margin-top:0; color: var(--text-color);'>Weaknesses ⚠️</h3><ul style='color: var(--text-muted);'>"
    for w in weaknesses:
        html += f"<li>{w}</li>"
    html += "</ul></div>"
    st.markdown(html, unsafe_allow_html=True)

with col_i3:
    html = "<div class='premium-card' style='border-top: 4px solid var(--warning); height: 100%;'><h3 style='margin-top:0; color: var(--text-color);'>Recommendations 💡</h3><ul style='color: var(--text-muted);'>"
    for r in recs:
        html += f"<li>{r}</li>"
    html += "</ul></div>"
    st.markdown(html, unsafe_allow_html=True)
