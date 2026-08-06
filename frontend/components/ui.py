import streamlit as st
from frontend.components.theme import (
    load_css,
    render_hero_banner,
    render_header,
    render_card as render_glass_card,
    render_badges,
    render_circular_progress,
    render_progress_bar,
    render_empty_state,
    render_alert,
    build_resume_text
)
from frontend.api_client import APIClient

def render_system_status():
    status = APIClient.check_health()
    
    # Status can return a dict of subsystem statuses, for now just check if backend is healthy
    is_healthy = bool(status)
    
    dot_class = "status-dot" if is_healthy else "status-dot offline"
    
    st.markdown(
        f"""
        <div style="position: fixed; bottom: 20px; right: 20px; background: var(--secondary-background-color); border: 1px solid #E5E7EB; border-radius: 12px; padding: 12px 20px; z-index: 9999; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); font-size: 0.8rem; display: flex; gap: 16px; font-weight: 500;">
            <div style="display: flex; align-items: center; gap: 8px; color: #6B7280;">
                <div class="{dot_class}"></div>Backend API
            </div>
            <div style="display: flex; align-items: center; gap: 8px; color: #6B7280;">
                <div class="{dot_class}"></div>Gemini Model
            </div>
            <div style="display: flex; align-items: center; gap: 8px; color: #6B7280;">
                <div class="{dot_class}"></div>FAISS
            </div>
            <div style="display: flex; align-items: center; gap: 8px; color: #6B7280;">
                <div class="{dot_class}"></div>Parser
            </div>
        </div>
        """, unsafe_allow_html=True
    )

def render_ai_explainability(section: str, reason: str, impact: str = "High", confidence: str = "95%"):
    st.markdown(
        f"""
        <div style="background-color: #FFFFFF; border-left: 4px solid var(--primary-color); padding: 1.5rem; border-radius: 4px 12px 12px 4px; margin-bottom: 1.5rem; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05); border-top: 1px solid #E5E7EB; border-right: 1px solid #E5E7EB; border-bottom: 1px solid #E5E7EB;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <strong style="font-size: 1.1rem; color: #111827;">{section} Updated</strong>
                <div style="display: flex; gap: 10px; font-size: 0.8rem;">
                    <span class="badge badge-success">ATS Impact: {impact}</span>
                    <span class="badge badge-primary">Confidence: {confidence}</span>
                </div>
            </div>
            <p style="margin: 0; font-size: 0.95rem; color: #6B7280;"><strong>Reason:</strong> {reason}</p>
        </div>
        """, unsafe_allow_html=True
    )

def render_radar_chart(metrics: dict):
    import plotly.graph_objects as go
    categories = list(metrics.keys())
    values = list(metrics.values())
    
    categories.append(categories[0])
    values.append(values[0])
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(37, 99, 235, 0.1)',
        line=dict(color='#2563EB', width=2)
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], color='#94a3b8', gridcolor='#e2e8f0'),
            angularaxis=dict(color='#475569', gridcolor='#e2e8f0')
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=20, b=20),
        height=300
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
