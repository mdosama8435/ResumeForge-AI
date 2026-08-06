import streamlit as st
from frontend.api_client import APIClient

def render_sidebar():
    # Hide default sidebar navigation
    st.markdown(
        """
        <style>
        [data-testid="stSidebarNav"] {display: none;}
        </style>
        """,
        unsafe_allow_html=True
    )
    
    with st.sidebar:
        # 1. Logo Block
        st.markdown(
            """
            <div style="display: flex; align-items: center; margin-bottom: 1rem; padding: 4px;">
                <div style="width: 44px; height: 44px; background: rgba(0,0,0,0.06); border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 1.4rem; margin-right: 12px; flex-shrink: 0;">
                    ✨
                </div>
                <div style="min-width: 0;">
                    <h3 style="margin: 0; font-size: 1.1rem; font-weight: 700; color: var(--text-color); white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">ResumeForge AI</h3>
                    <div style="font-size: 0.85rem; color: #4B5563; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">Guest workspace</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("<hr style='margin: 0.5rem 0 1rem 0; border-color: rgba(0,0,0,0.1);' />", unsafe_allow_html=True)
        
        # 2. WORKFLOW Navigation
        st.markdown("<div style='font-size: 0.75rem; font-weight: 700; color: #4B5563; margin-bottom: 0.5rem; letter-spacing: 0.05em;'>WORKFLOW</div>", unsafe_allow_html=True)
        
        st.page_link("app.py", label="App", icon=":material/grid_view:")
        st.page_link("pages/02_Upload.py", label="Upload", icon=":material/upload:")
        st.page_link("pages/03_ATS_Analysis.py", label="ATS analysis", icon=":material/adjust:")
        st.page_link("pages/04_Resume_Optimizer.py", label="Resume optimizer", icon=":material/tune:")
        st.page_link("pages/05_Resume_Preview.py", label="Resume preview", icon=":material/description:")
        st.page_link("pages/06_Cover_Letter.py", label="Cover letter", icon=":material/mail:")
        st.page_link("pages/07_Interview_Questions.py", label="Interview questions", icon=":material/chat_bubble_outline:")
        
        if st.session_state.get("settings_enabled", True): # Assume Settings exists or will exist
            try:
                st.page_link("pages/08_Settings.py", label="Settings", icon=":material/settings:")
            except Exception:
                pass
        
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        
        # 3. SYSTEM STATUS
        st.markdown("<div style='font-size: 0.75rem; font-weight: 700; color: #4B5563; margin-bottom: 0.5rem; letter-spacing: 0.05em;'>SYSTEM STATUS</div>", unsafe_allow_html=True)
        
        status = APIClient.check_health()
        is_healthy = bool(status)
        dot_class = "status-dot" if is_healthy else "status-dot offline"
        
        st.markdown(
            f'''
            <div style="padding: 12px; background: rgba(0,0,0,0.05); border-radius: 8px; margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; gap: 8px;">
                    <span style="font-size: 0.95rem; color: var(--text-color); white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">Backend API</span>
                    <div class="{dot_class}" style="flex-shrink: 0;"></div>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; gap: 8px;">
                    <span style="font-size: 0.95rem; color: var(--text-color); white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">Gemini model</span>
                    <div class="{dot_class}" style="flex-shrink: 0;"></div>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; gap: 8px;">
                    <span style="font-size: 0.95rem; color: var(--text-color); white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">FAISS vector DB</span>
                    <div class="{dot_class}" style="flex-shrink: 0;"></div>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; gap: 8px;">
                    <span style="font-size: 0.95rem; color: var(--text-color); white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">Parser engine</span>
                    <div class="{dot_class}" style="flex-shrink: 0;"></div>
                </div>
            </div>
            ''', unsafe_allow_html=True
        )
        
        st.markdown("<hr style='margin: 1rem 0; border-color: rgba(0,0,0,0.1);' />", unsafe_allow_html=True)
        
        # 4. Profile
        user_name = "Guest user"
        user_initials = "GU"
        
        if "resume_data" in st.session_state and st.session_state.resume_data.get("text"):
            lines = [line.strip() for line in st.session_state.resume_data["text"].split("\n") if line.strip()]
            if lines:
                name = lines[0]
                if len(name) < 30:
                    user_name = name
                    parts = name.split()
                    if len(parts) >= 2:
                        user_initials = (parts[0][0] + parts[-1][0]).upper()
                    else:
                        user_initials = parts[0][:2].upper()

        st.markdown(
            f"""
            <div style="display: flex; align-items: center; padding: 4px;">
                <div style="width: 36px; height: 36px; border-radius: 50%; background: rgba(0,0,0,0.08); margin-right: 12px; display: flex; align-items: center; justify-content: center; font-size: 0.9rem; font-weight: 700; color: var(--text-color); flex-shrink: 0;">
                    {user_initials}
                </div>
                <div style="min-width: 0; overflow: hidden;">
                    <div style="font-size: 0.95rem; font-weight: 700; color: var(--text-color); line-height: 1.2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{user_name}</div>
                    <div style="font-size: 0.85rem; color: #4B5563; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">Enterprise plan</div>
                </div>
            </div>
            <div style="text-align: center; font-size: 0.8rem; margin-top: 16px; color: #4B5563;">
                Version v2.0.0-enterprise
            </div>
            """, unsafe_allow_html=True
        )
