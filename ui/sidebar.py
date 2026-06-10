"""Sidebar component for CodeSage AI."""
import streamlit as st
import os


def render_sidebar():
    """Render the main app sidebar."""

    # ── Sidebar collapse button — clean chevron icon ──────────────────────────
    st.markdown("""
    <style>
    /* Kill every child element inside the collapse button */
    [data-testid="collapsedControl"] * {
        display: none !important;
    }

    /* Button shape */
    [data-testid="collapsedControl"] {
        background: #131929 !important;
        border: 1px solid #1e2a45 !important;
        border-radius: 50% !important;
        width: 28px !important;
        height: 28px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
        position: relative !important;
        overflow: hidden !important;
        transition: border-color 0.2s, box-shadow 0.2s !important;
    }
    [data-testid="collapsedControl"]:hover {
        border-color: #00d4ff !important;
        box-shadow: 0 0 10px rgba(0,212,255,0.25) !important;
    }

    /* ‹ when sidebar is OPEN — click will collapse it */
    [data-testid="stSidebar"][aria-expanded="true"] [data-testid="collapsedControl"]::after,
    [data-testid="stSidebar"] [data-testid="collapsedControl"]::after {
        content: '‹' !important;
        display: block !important;
        color: #00d4ff !important;
        font-size: 22px !important;
        line-height: 1 !important;
        position: absolute !important;
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%) !important;
    }

    /* › when sidebar is COLLAPSED — click will expand it */
    [data-testid="collapsedControl"]::after {
        content: '›' !important;
        display: block !important;
        color: #00d4ff !important;
        font-size: 22px !important;
        line-height: 1 !important;
        position: absolute !important;
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        # ── Logo ──────────────────────────────────────────────────────────────
        st.markdown("""
        <div style='text-align:center; padding: 1.25rem 0 1.5rem'>
            <svg width="44" height="44" viewBox="0 0 40 40" fill="none"
                 xmlns="http://www.w3.org/2000/svg"
                 style='margin:0 auto; display:block; margin-bottom:0.6rem'>
                <circle cx="20" cy="20" r="18" stroke="url(#grad)" stroke-width="2"/>
                <path d="M20 8v24M14 20h12M17 14l6 12M23 14l-6 12"
                      stroke="url(#grad)" stroke-width="1.5" stroke-linecap="round"/>
                <defs>
                    <linearGradient id="grad" x1="0" y1="0" x2="40" y2="40">
                        <stop offset="0%" stop-color="#00d4ff"/>
                        <stop offset="100%" stop-color="#7c3aed"/>
                    </linearGradient>
                </defs>
            </svg>
            <div style='font-size:1.25rem; font-weight:800;
                 background:linear-gradient(135deg,#00d4ff,#7c3aed);
                 -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                 letter-spacing:-0.3px'>CodeSage AI</div>
            <div style='color:#4a5568; font-size:0.72rem; margin-top:3px;
                 letter-spacing:0.5px; text-transform:uppercase'>Intelligent Code Review</div>
        </div>
        """, unsafe_allow_html=True)

        # ── User info ──────────────────────────────────────────────────────────
        user = st.session_state.get("user")
        if user:
            name   = user.get("full_name") or user.get("email", "User")
            avatar = user.get("avatar_url", "")
            avatar_html = (
                f'<img src="{avatar}" style="width:34px;height:34px;border-radius:50%;object-fit:cover">'
                if avatar else
                f'<div style="width:34px;height:34px;border-radius:50%;background:linear-gradient(135deg,#7c3aed,#00d4ff);'
                f'display:flex;align-items:center;justify-content:center;font-weight:700;font-size:0.9rem;color:#fff">'
                f'{name[0].upper()}</div>'
            )
            st.markdown(f"""
            <div style='background:#131929; border:1px solid #1e2a45; border-radius:10px;
                 padding:0.7rem 0.85rem; margin-bottom:1.1rem;
                 display:flex; align-items:center; gap:0.75rem'>
                {avatar_html}
                <div style='min-width:0'>
                    <div style='color:#e8eaf6; font-size:0.85rem; font-weight:600;
                         white-space:nowrap; overflow:hidden; text-overflow:ellipsis'>{name}</div>
                    <div style='color:#4a5568; font-size:0.72rem;
                         white-space:nowrap; overflow:hidden; text-overflow:ellipsis'>{user.get("email","")}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ── API Configuration ──────────────────────────────────────────────────
        _ENV_GROQ_KEY   = os.getenv("GROQ_API_KEY", "")
        _ENV_GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")

        provider = st.selectbox("Provider", ["Groq", "Gemini"], key="provider")

        if provider == "Groq":
            st.selectbox("Model", [
                "llama-3.3-70b-versatile",
                "llama-3.1-8b-instant",
                "mixtral-8x7b-32768",
                "gemma2-9b-it",
            ], key="model")
            api_link = "https://console.groq.com/keys"
            env_key  = _ENV_GROQ_KEY
        else:
            st.selectbox("Model", [
                "gemini-2.0-flash",
                "gemini-1.5-flash",
                "gemini-1.5-pro",
            ], key="model")
            api_link = "https://aistudio.google.com/app/apikey"
            env_key  = _ENV_GEMINI_KEY

        if not env_key:
            st.markdown("""
            <div style='display:flex; align-items:center; gap:0.5rem;
                 margin:0.75rem 0 0.4rem'>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none"
                     stroke="#00d4ff" stroke-width="2">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                    <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                </svg>
                <span style='color:#e8eaf6; font-weight:600; font-size:0.85rem'>API Key</span>
            </div>
            """, unsafe_allow_html=True)
            st.text_input(
                "API Key",
                type="password",
                placeholder="Paste your API key",
                key="api_key",
                label_visibility="collapsed",
            )
            st.markdown(
                f"<a href='{api_link}' target='_blank' style='display:inline-flex; align-items:center; "
                f"gap:0.35rem; color:#7c3aed; font-size:0.78rem; text-decoration:none; margin-top:4px'>"
                f"<svg width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2'>"
                f"<path d='M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6'/>"
                f"<polyline points='15 3 21 3 21 9'/><line x1='10' y1='14' x2='21' y2='3'/></svg>"
                f"Get free API key</a>",
                unsafe_allow_html=True,
            )

        st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)
        st.markdown("---")

        # ── Session Stats ──────────────────────────────────────────────────────
        st.markdown("""
        <div style='display:flex; align-items:center; gap:0.5rem; margin:0.75rem 0 0.85rem'>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none"
                 stroke="#00d4ff" stroke-width="2">
                <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
            </svg>
            <span style='color:#e8eaf6; font-weight:600; font-size:0.85rem'>Session Stats</span>
        </div>
        """, unsafe_allow_html=True)

        reviews_done = len(st.session_state.get("review_history", []))
        chats_done   = len(st.session_state.get("chat_history", []))

        st.markdown(f"""
        <div style='display:grid; grid-template-columns:1fr 1fr; gap:0.5rem; margin-bottom:0.5rem'>
            <div class='metric-card'>
                <div class='metric-number' style='color:#00d4ff; font-size:1.4rem'>{reviews_done}</div>
                <div class='metric-label'>Reviews</div>
            </div>
            <div class='metric-card'>
                <div class='metric-number' style='color:#7c3aed; font-size:1.4rem'>{chats_done}</div>
                <div class='metric-label'>Chats</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Recent history ─────────────────────────────────────────────────────
        if reviews_done > 0:
            st.markdown("---")
            st.markdown("""
            <div style='display:flex; align-items:center; gap:0.5rem; margin:0.75rem 0 0.85rem'>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none"
                     stroke="#00d4ff" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <polyline points="12 6 12 12 16 14"/>
                </svg>
                <span style='color:#e8eaf6; font-weight:600; font-size:0.85rem'>Recent Reviews</span>
            </div>
            """, unsafe_allow_html=True)

            for item in reversed(st.session_state.review_history[-5:]):
                st.markdown(f"""
                <div class='history-item'>
                    <span class='lang-pill'>{item['language']}</span>
                    <span style='color:#8892b0; font-size:0.78rem; margin-left:0.5rem'>{item['time']}</span>
                    <div style='color:#e8eaf6; font-size:0.82rem; margin-top:4px;
                         white-space:nowrap; overflow:hidden; text-overflow:ellipsis'>{item['feature']}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")

        # ── Action buttons ─────────────────────────────────────────────────────
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Clear", use_container_width=True, key="btn_clear"):
                st.session_state.review_history = []
                st.session_state.chat_history   = []
                st.session_state.last_result    = None
                st.rerun()
        with col2:
            if st.button("Logout", use_container_width=True, key="btn_logout"):
                for key in ["user", "access_token", "review_history", "chat_history", "last_result"]:
                    st.session_state.pop(key, None)
                st.rerun()