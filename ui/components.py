"""Reusable UI components for CodeSage AI."""
import streamlit as st


# Font Awesome CDN - Add this to your _config.toml or inject in your app
def load_icons():
    """Load Font Awesome icons stylesheet."""
    st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    """, unsafe_allow_html=True)


def hero_banner():
    load_icons()
    st.markdown("""
    <div class='hero-banner'>
        <h1 class='hero-title'><i class="fas fa-flask"></i> CodeSage AI</h1>
        <p class='hero-sub'>Enterprise-grade code review, security auditing, documentation & refactoring — powered by LLMs</p>
    </div>
    """, unsafe_allow_html=True)


def check_code(code_input: str) -> bool:
    if not code_input.strip():
        st.warning("<i class='fas fa-exclamation-triangle'></i> Please paste some code first!", icon="⚠️")
        return False
    return True


def save_history(feature: str, language: str, code_input: str):
    from datetime import datetime
    st.session_state.review_history.append({
        "feature": feature,
        "language": language,
        "time": datetime.now().strftime("%H:%M"),
        "code_preview": code_input[:80]
    })


def security_notice():
    load_icons()
    st.markdown("""
    <div style='background:rgba(255,71,87,0.08); border:1px solid rgba(255,71,87,0.2);
         border-radius:8px; padding:0.75rem 1rem; margin-bottom:1rem'>
        <span style='color:#ff4757; font-size:1.1rem'><i class="fas fa-lock"></i></span>
        <span style='color:#8892b0; font-size:0.9rem'>
            Performs OWASP-aligned security analysis. Results are advisory — always verify with dedicated security tools.
        </span>
    </div>
    """, unsafe_allow_html=True)


def chat_message(role: str, content: str):
    load_icons()
    
    if role == "user":
        role_icon = '<i class="fas fa-user" style="color:#7c3aed"></i>'
        bg = "rgba(124,58,237,0.1)"
        label = "You"
    else:
        role_icon = '<i class="fas fa-flask-vial" style="color:#00d4ff"></i>'
        bg = "rgba(0,212,255,0.05)"
        label = "CodeSage"
    
    st.markdown(f"""
    <div style='background:{bg}; border-radius:10px; padding:0.75rem 1rem; margin:0.5rem 0'>
        <div style='color:#4a5568; font-size:0.85rem; margin-bottom:4px'>{role_icon} <strong>{label}</strong></div>
        <div style='color:#e8eaf6; line-height:1.5'>{content}</div>
    </div>
    """, unsafe_allow_html=True)


def footer():
    st.markdown("---")
    st.markdown("""
    <div style='text-align:center; color:#2d3748; font-size:0.8rem; padding:1rem 0'>
        <i class="fas fa-cube"></i> CodeSage AI · Built with Streamlit · Powered by Groq & Gemini
    </div>
    """, unsafe_allow_html=True)