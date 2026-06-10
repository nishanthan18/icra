"""Reusable UI components for CodeSage AI."""
import streamlit as st


def hero_banner():
    st.markdown("""
    <div class='hero-banner'>
        <div style='display:flex; align-items:center; gap:0.75rem; margin-bottom:0.4rem'>
            <svg width="32" height="32" viewBox="0 0 40 40" fill="none"
                 xmlns="http://www.w3.org/2000/svg">
                <circle cx="20" cy="20" r="18" stroke="url(#hgrad)" stroke-width="2"/>
                <path d="M20 8v24M14 20h12M17 14l6 12M23 14l-6 12"
                      stroke="url(#hgrad)" stroke-width="1.5" stroke-linecap="round"/>
                <defs>
                    <linearGradient id="hgrad" x1="0" y1="0" x2="40" y2="40">
                        <stop offset="0%" stop-color="#00d4ff"/>
                        <stop offset="100%" stop-color="#7c3aed"/>
                    </linearGradient>
                </defs>
            </svg>
            <h1 class='hero-title'>CodeSage AI</h1>
        </div>
        <p class='hero-sub'>
            Enterprise-grade code review, security auditing, documentation &amp;
            refactoring — powered by LLMs
        </p>
    </div>
    """, unsafe_allow_html=True)


def check_code(code_input: str) -> bool:
    if not code_input.strip():
        st.warning("⚠️ Please paste some code first!")
        return False
    return True


def save_history(feature: str, language: str, code_input: str, result: str = ""):
    from datetime import datetime
    st.session_state.review_history.append({
        "feature": feature,
        "language": language,
        "time": datetime.now().strftime("%H:%M"),
        "code_preview": code_input[:80],
    })


def security_notice():
    st.markdown("""
    <div style='background:rgba(255,71,87,0.08); border:1px solid rgba(255,71,87,0.2);
         border-radius:8px; padding:0.75rem 1rem; margin-bottom:1rem;
         display:flex; align-items:center; gap:0.6rem'>
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none"
             stroke="#ff4757" stroke-width="2">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
        </svg>
        <span style='color:#8892b0; font-size:0.88rem'>
            Performs OWASP-aligned security analysis. Results are advisory —
            always verify with dedicated security tools.
        </span>
    </div>
    """, unsafe_allow_html=True)


def chat_message(role: str, content: str):
    is_user = role == "user"
    bg      = "rgba(124,58,237,0.1)" if is_user else "rgba(0,212,255,0.05)"
    border  = "rgba(124,58,237,0.25)" if is_user else "rgba(0,212,255,0.15)"
    label   = "You" if is_user else "CodeSage"
    icon_svg = (
        # user icon
        '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" '
        'stroke="#a78bfa" stroke-width="2">'
        '<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>'
        '<circle cx="12" cy="7" r="4"/></svg>'
        if is_user else
        # bot / sage icon
        '<svg width="14" height="14" viewBox="0 0 40 40" fill="none" '
        'xmlns="http://www.w3.org/2000/svg">'
        '<circle cx="20" cy="20" r="18" stroke="#00d4ff" stroke-width="2"/>'
        '<path d="M20 8v24M14 20h12" stroke="#00d4ff" stroke-width="1.5" '
        'stroke-linecap="round"/></svg>'
    )
    label_color = "#a78bfa" if is_user else "#00d4ff"

    st.markdown(f"""
    <div style='background:{bg}; border:1px solid {border}; border-radius:10px;
         padding:0.75rem 1rem; margin:0.5rem 0'>
        <div style='display:flex; align-items:center; gap:0.4rem;
             margin-bottom:6px'>
            {icon_svg}
            <span style='color:{label_color}; font-size:0.75rem;
                  font-weight:600; letter-spacing:0.3px'>{label}</span>
        </div>
        <div style='color:#e8eaf6; font-size:0.9rem; line-height:1.55'>{content}</div>
    </div>
    """, unsafe_allow_html=True)


def footer():
    st.markdown("---")
    st.markdown("""
    <div style='text-align:center; padding:0.75rem 0 1rem;
         display:flex; align-items:center; justify-content:center; gap:0.5rem'>
        <svg width="14" height="14" viewBox="0 0 40 40" fill="none"
             xmlns="http://www.w3.org/2000/svg" style='opacity:0.4'>
            <circle cx="20" cy="20" r="18" stroke="#00d4ff" stroke-width="2"/>
            <path d="M20 8v24M14 20h12" stroke="#00d4ff"
                  stroke-width="1.5" stroke-linecap="round"/>
        </svg>
        <span style='color:#2d3748; font-size:0.78rem'>
            CodeSage AI &nbsp;·&nbsp; Built with Streamlit
            &nbsp;·&nbsp; Powered by Groq &amp; Gemini
        </span>
    </div>
    """, unsafe_allow_html=True)