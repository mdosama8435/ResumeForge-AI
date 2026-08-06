import streamlit as st

def load_css():
    st.markdown("""
        <style>
        /* Base typography and spacing */
        .text-main { color: var(--text-color); }
        .text-muted { color: #6B7280; }
        
        /* Main layout overrides */
        header[data-testid="stHeader"] { display: none !important; }
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 2rem !important;
            max-width: 1200px !important;
        }
        
        /* Premium Card */
        .premium-card {
            background: linear-gradient(145deg, #ffffff, #f8fafc) !important;
            border: 1px solid #e2e8f0 !important;
            border-top: 4px solid #4F46E5 !important;
            border-radius: 16px !important;
            padding: 28px !important;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05) !important;
            margin-bottom: 1.5rem !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        .premium-card:hover {
            transform: translateY(-5px) scale(1.01) !important;
            box-shadow: 0 20px 40px rgba(79, 70, 229, 0.12) !important;
            border-color: #c7d2fe !important;
            border-top: 4px solid #7C3AED !important;
        }
        
        /* Gradient Text */
        .gradient-text {
            background: linear-gradient(135deg, var(--primary-color), #7C3AED);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: inline-block;
        }
        
        /* Modern Buttons */
        .stButton > button {
            border-radius: 8px !important;
            border: 2px solid transparent !important;
            background: linear-gradient(135deg, #4F46E5, #4338CA) !important;
            color: white !important;
            font-weight: 600 !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.3) !important;
        }
        .stButton > button:hover {
            transform: translateY(-2px) scale(1.02) !important;
            box-shadow: 0 10px 20px -3px rgba(79, 70, 229, 0.5) !important;
            background: linear-gradient(135deg, #4338CA, #3730A3) !important;
            border-color: rgba(255, 255, 255, 0.2) !important;
        }
        .stButton > button p {
            color: white !important;
        }
        
        /* Badges */
        .badge {
            display: inline-flex;
            align-items: center;
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-right: 8px;
            margin-bottom: 8px;
        }
        .badge-success { background: rgba(34, 197, 94, 0.1); color: #15803d; border: 1px solid rgba(34, 197, 94, 0.2); }
        .badge-warning { background: rgba(245, 158, 11, 0.1); color: #b45309; border: 1px solid rgba(245, 158, 11, 0.2); }
        .badge-danger { background: rgba(239, 68, 68, 0.1); color: #b91c1c; border: 1px solid rgba(239, 68, 68, 0.2); }
        .badge-primary { background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; }
        
        /* Circular Progress */
        .circular-chart { display: block; margin: 10px auto; max-width: 80%; max-height: 250px; }
        .circle-bg { fill: none; stroke: #E5E7EB; stroke-width: 3.8; }
        .circle { fill: none; stroke-width: 2.8; stroke-linecap: round; animation: progress 1.5s ease-out forwards; }
        @keyframes progress { 0% { stroke-dasharray: 0 100; } }
        .circular-chart.success .circle { stroke: #22C55E; }
        .circular-chart.warning .circle { stroke: #F59E0B; }
        .circular-chart.danger .circle { stroke: #EF4444; }
        .percentage { fill: var(--text-color); font-weight: 800; font-size: 0.5em; text-anchor: middle; }
        
        /* Status Dot */
        .status-dot {
            width: 8px; height: 8px; border-radius: 50%;
            background: #22C55E;
        }
        .status-dot.offline {
            background: #EF4444;
        }
        
        /* Expanders overrides */
        .streamlit-expanderHeader {
            background-color: var(--secondary-background-color);
            border: 1px solid #E5E7EB;
            border-radius: 8px;
            color: var(--text-color);
        }
        </style>
    """, unsafe_allow_html=True)

def render_hero_banner(title: str, subtitle: str, description: str):
    html_content = f"""
<div style="text-align: center; padding: 4rem 2rem; background: linear-gradient(135deg, rgba(79, 70, 229, 0.08), rgba(124, 58, 237, 0.03)); border-radius: 24px; border: 1px solid rgba(79, 70, 229, 0.15); margin-bottom: 2rem; margin-top: 0;">
<h1 class="gradient-text" style="font-size: 4.5rem; margin-bottom: 1rem; font-weight: 900; line-height: 1.1; letter-spacing: -1px;">{title}</h1>
<h2 style="font-size: 2.2rem; margin-bottom: 1.5rem; color: #1e293b; font-weight: 700;">{subtitle}</h2>
<p style="font-size: 1.25rem; max-width: 750px; margin: 0 auto 1.5rem auto; color: #475569; line-height: 1.6;">{description}</p>
</div>
"""
    st.markdown(html_content, unsafe_allow_html=True)

def render_header(title: str, description: str, icon: str = ""):
    icon_html = f"<span style='margin-right: 15px;'>{icon}</span>" if icon else ""
    st.markdown(
        f"""
        <div style="margin-bottom: 2rem;">
            <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem; color: var(--text-color);">{icon_html}{title}</h1>
            <p style="font-size: 1.1rem; color: #6B7280;">{description}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_card(title: str, content: str, icon: str = ""):
    icon_html = f"""
<div style="display: inline-flex; align-items: center; justify-content: center; width: 48px; height: 48px; border-radius: 12px; background: linear-gradient(135deg, rgba(79, 70, 229, 0.1), rgba(124, 58, 237, 0.1)); font-size: 1.5rem; margin-bottom: 16px;">
{icon}
</div>
""" if icon else ""
    html_content = f"""
<div class="premium-card">
{icon_html}
<h3 style="margin-top: 0; color: #0f172a; font-size: 1.25rem; font-weight: 700; margin-bottom: 12px;">{title}</h3>
<div style="color: #475569; font-size: 0.95rem; line-height: 1.6;">{content}</div>
</div>
"""
    st.markdown(html_content, unsafe_allow_html=True)

def render_badges(items: list, badge_type: str = "success"):
    if not items:
        return
    badges_html = "".join([f"<span class='badge badge-{badge_type}'>{item}</span>" for item in items])
    st.markdown(f"<div>{badges_html}</div>", unsafe_allow_html=True)

def render_circular_progress(percentage: int, title: str):
    stroke_dasharray = f"{percentage}, 100"
    color_class = "success" if percentage >= 75 else ("warning" if percentage >= 50 else "danger")
    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 1.5rem;">
            <svg viewBox="0 0 36 36" class="circular-chart {color_class}">
                <path class="circle-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                <path class="circle" stroke-dasharray="{stroke_dasharray}" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                <text x="18" y="20.35" class="percentage">{percentage}%</text>
            </svg>
            <h4 style="color: var(--text-color); margin-top: 1rem;">{title}</h4>
        </div>
    """, unsafe_allow_html=True)

def render_progress_bar(label: str, percentage: int):
    color = "#22C55E" if percentage >= 80 else ("#F59E0B" if percentage >= 50 else "#EF4444")
    st.markdown(f"""
        <div style="margin-bottom: 1.2rem;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                <span style="font-size: 0.95rem; font-weight: 600; color: var(--text-color);">{label}</span>
                <span style="font-size: 0.95rem; font-weight: 700; color: {color};">{percentage}%</span>
            </div>
            <div style="width: 100%; background-color: #E5E7EB; border-radius: 9999px; height: 10px;">
                <div style="background-color: {color}; height: 10px; border-radius: 9999px; width: {percentage}%;"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_empty_state(title: str, description: str, icon: str = "🚀"):
    st.markdown(f"""
        <div class="premium-card" style="text-align: center; border: 2px dashed #E5E7EB; padding: 4rem 2rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">{icon}</div>
            <h3 style="color: var(--text-color); margin-bottom: 0.5rem;">{title}</h3>
            <p style="color: #6B7280; max-width: 400px; margin: 0 auto;">{description}</p>
        </div>
    """, unsafe_allow_html=True)

def render_alert(title: str, message: str, type: str = "success"):
    border_color = "#22C55E" if type == "success" else ("#F59E0B" if type == "warning" else "#EF4444")
    bg_color = "rgba(34, 197, 94, 0.1)" if type == "success" else ("rgba(245, 158, 11, 0.1)" if type == "warning" else "rgba(239, 68, 68, 0.1)")
    st.markdown(f"""
        <div style="background-color: {bg_color}; border-left: 4px solid {border_color}; padding: 1rem; border-radius: 4px; margin-bottom: 1rem;">
            <strong style="color: var(--text-color);">{title}</strong>
            <p style="color: #6B7280; margin: 0.5rem 0 0 0;">{message}</p>
        </div>
    """, unsafe_allow_html=True)

def build_resume_text(opt_data: dict) -> str:
    """Build a plain text representation of the optimized resume from structured data."""
    if not opt_data:
        return "No optimized data available."
    
    lines = []
    if summary := opt_data.get("summary"):
        lines.append("PROFESSIONAL SUMMARY")
        lines.append("-" * 20)
        lines.append(summary)
        lines.append("")
        
    if skills := opt_data.get("skills"):
        lines.append("SKILLS")
        lines.append("-" * 6)
        lines.append(", ".join(skills))
        lines.append("")
        
    if experience := opt_data.get("experience"):
        lines.append("EXPERIENCE")
        lines.append("-" * 10)
        for exp in experience:
            lines.append(f"- {exp}")
        lines.append("")
        
    if projects := opt_data.get("projects"):
        lines.append("PROJECTS")
        lines.append("-" * 8)
        for proj in projects:
            lines.append(f"- {proj}")
        lines.append("")
        
    return "\n".join(lines) if lines else "No optimized sections found."
