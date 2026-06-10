"""
CodeSage AI — Main Entry Point
================================
Run with:  streamlit run app.py
"""
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ── Page config (must be first Streamlit call) ──────────────────────────────
st.set_page_config(
    page_title="CodeSage AI",
    page_icon="assets/icon.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Bootstrapping ────────────────────────────────────────────────────────────
from utils.session import init_session
init_session()

# ── Google OAuth callback (check before rendering anything) ─────────────────
from auth.google_auth import handle_google_callback

if handle_google_callback():
    st.rerun()

# ── Route to auth pages if not logged in ────────────────────────────────────
from auth.auth_guard import is_authenticated

if not is_authenticated():
    page = st.query_params.get("page", "login")
    if page == "signup":
        from auth.signup import render_signup
        render_signup()
    elif page == "forgot":
        from auth.forgot_password import render_forgot_password
        render_forgot_password()
    else:
        from auth.login import render_login
        render_login()
    st.stop()

# ── Authenticated: render main app ───────────────────────────────────────────
from ui.styles import MAIN_CSS
from ui.sidebar import render_sidebar
from ui.components import hero_banner, check_code, footer

from utils.history import save_history

from features.review import full_review
from features.refactor import generate_refactored
from features.docs import generate_docs
from features.security import find_security
from features.explain import explain_code
from features.complexity import complexity_analysis
from features.tests import generate_tests
from features.translate import translate_code
from features.chat import chat_about_code

# ── Inject Font Awesome + icon helper styles ─────────────────────────────────
FA_CDN = """
<link rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css"
      crossorigin="anonymous" referrerpolicy="no-referrer" />
<style>
  .fa-icon-label { display:inline-flex; align-items:center; gap:0.5rem; font-weight:600; margin-bottom:0.5rem; }
  .fa-icon-label i { font-size:0.95em; opacity:0.85; }
</style>
"""
st.markdown(FA_CDN, unsafe_allow_html=True)
st.markdown(MAIN_CSS, unsafe_allow_html=True)

render_sidebar()
hero_banner()

# ── Code Input & Settings ────────────────────────────────────────────────────
col_in, col_cfg = st.columns([3, 1], gap="large")

with col_in:
    st.markdown(
        '<p class="fa-icon-label"><i class="fa-regular fa-file-code"></i> Code Input</p>',
        unsafe_allow_html=True,
    )
    code_input = st.text_area(
        label="code_area",
        label_visibility="collapsed",
        placeholder="# Paste your code here...\n\ndef example():\n    pass",
        height=300,
        key="code_input",
    )

with col_cfg:
    st.markdown(
        '<p class="fa-icon-label"><i class="fa-solid fa-sliders"></i> Settings</p>',
        unsafe_allow_html=True,
    )
    language = st.selectbox("Language", [
        "Python", "JavaScript", "TypeScript", "Java", "C++", "C", "Go",
        "Rust", "C#", "PHP", "Ruby", "Swift", "Kotlin", "SQL", "Shell",
        "R", "Scala", "Dart", "Haskell", "Other",
    ])
    st.markdown("<div style='margin-top: 0.5rem;'></div>", unsafe_allow_html=True)
    review_depth = st.select_slider("Review Depth", ["Quick", "Standard", "Deep Dive"], value="Standard")
    st.markdown("<div style='margin-top: 0.5rem;'></div>", unsafe_allow_html=True)
    context = st.text_input("Context (optional)", placeholder="What does this code do?")

# ── Spacer before tabs ────────────────────────────────────────────────────────
st.markdown("<div style='margin: 2.5rem 0 0 0;'></div>", unsafe_allow_html=True)

# ── Feature Tabs ─────────────────────────────────────────────────────────────
tabs = st.tabs([
    "Full Review", "Refactor", "Docs", "Security",
    "Explain", "Complexity", "Tests", "Translate", "Chat",
])

# ── Tab 1: Full Review ───────────────────────────────────────────────────────
with tabs[0]:
    st.markdown(
        '<p class="fa-icon-label"><i class="fa-solid fa-magnifying-glass-chart"></i> Full Review</p>',
        unsafe_allow_html=True,
    )
    st.caption("Comprehensive code review covering quality, bugs, style, and best practices.")
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    if st.button("Run Full Review", use_container_width=True, key="btn_review"):
        if check_code(code_input):
            with st.spinner("Analyzing code..."):
                result = full_review(code_input, language, context, review_depth)
            if result:
                save_history("Full Review", language, code_input, result)
                st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
                st.markdown(result)

# ── Tab 2: Refactor ──────────────────────────────────────────────────────────
with tabs[1]:
    st.markdown(
        '<p class="fa-icon-label"><i class="fa-solid fa-wand-magic-sparkles"></i> Refactor</p>',
        unsafe_allow_html=True,
    )
    refactor_focus = st.multiselect(
        "Refactoring Goals",
        ["Readability", "Performance", "DRY principle", "SOLID principles", "Error handling",
         "Type safety", "Modularity", "Naming conventions", "Modern syntax", "Memory efficiency"],
        default=["Readability", "Performance"],
    )
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    if st.button("Refactor Code", use_container_width=True, key="btn_refactor"):
        if check_code(code_input):
            with st.spinner("Refactoring..."):
                result = generate_refactored(code_input, language, refactor_focus)
            if result:
                save_history("Refactor", language, code_input, result)
                st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
                st.markdown(result)

# ── Tab 3: Documentation ─────────────────────────────────────────────────────
with tabs[2]:
    st.markdown(
        '<p class="fa-icon-label"><i class="fa-solid fa-book-open"></i> Documentation</p>',
        unsafe_allow_html=True,
    )
    doc_style_map = {
        "Python": ["Google Style", "NumPy Style", "Sphinx/RST", "Epytext"],
        "JavaScript": ["JSDoc", "TSDoc"],
        "TypeScript": ["TSDoc", "JSDoc"],
        "Java": ["Javadoc"],
    }
    available_styles = doc_style_map.get(language, ["Generic Docstring", "JSDoc", "Google Style"])
    doc_style = st.selectbox("Documentation Style", available_styles)
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

    if st.button("Generate Docs", use_container_width=True, key="btn_docs"):
        if check_code(code_input):
            with st.spinner("Generating documentation..."):
                result = generate_docs(code_input, language, doc_style)
            if result:
                save_history("Documentation", language, code_input, result)
                st.session_state["docs_result"] = result
                st.session_state["docs_style"] = doc_style
                st.session_state["docs_language"] = language

    if st.session_state.get("docs_result"):
        result       = st.session_state["docs_result"]
        cached_style = st.session_state.get("docs_style", doc_style)
        cached_lang  = st.session_state.get("docs_language", language)

        st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
        st.markdown(result)
        st.markdown("---")

        ext_map  = {"Sphinx/RST": "rst", "Javadoc": "java", "JSDoc": "js", "TSDoc": "ts"}
        file_ext = ext_map.get(cached_style, "md")

        col_dl1, col_dl2, _ = st.columns([1, 1, 2])

        with col_dl1:
            st.download_button(
                label="Download as Markdown",
                data=result.encode("utf-8"),
                file_name=f"docs_{cached_lang.lower()}.md",
                mime="text/markdown",
                use_container_width=True,
                key="dl_md",
            )

        with col_dl2:
            st.download_button(
                label="Download as Text",
                data=result.encode("utf-8"),
                file_name=f"docs_{cached_lang.lower()}.txt",
                mime="text/plain",
                use_container_width=True,
                key="dl_txt",
            )

        st.markdown(
            """
            <style>
            div[data-testid="stDownloadButton"] button::before {
                font-family: "Font Awesome 6 Free";
                font-weight: 900;
                content: "\\f019\\00a0";
                margin-right: 2px;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

# ── Tab 4: Security ───────────────────────────────────────────────────────────
with tabs[3]:
    st.markdown(
        '<p class="fa-icon-label"><i class="fa-solid fa-shield-halved"></i> Security Audit</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div style='background:rgba(255,71,87,0.08); border:1px solid rgba(255,71,87,0.2);
             border-radius:8px; padding:0.85rem 1.1rem; margin-bottom:1.25rem;
             display:flex; align-items:center; gap:0.6rem;'>
            <i class="fa-solid fa-triangle-exclamation" style='color:#ff4757;'></i>
            <span style='color:#8892b0; font-size:0.9rem'>
                OWASP-aligned security analysis. Results are advisory — always verify with dedicated tools.
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div style='margin-top: 0.5rem;'></div>", unsafe_allow_html=True)
    if st.button("Run Security Audit", use_container_width=True, key="btn_security"):
        if check_code(code_input):
            with st.spinner("Running security audit..."):
                result = find_security(code_input, language)
            if result:
                save_history("Security Audit", language, code_input, result)
                st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
                st.markdown(result)

# ── Tab 5: Explain ────────────────────────────────────────────────────────────
with tabs[4]:
    st.markdown(
        '<p class="fa-icon-label"><i class="fa-solid fa-lightbulb"></i> Explain Code</p>',
        unsafe_allow_html=True,
    )
    explain_level = st.radio("Audience Level", ["Beginner", "Intermediate", "Expert"], horizontal=True)
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    if st.button("Explain Code", use_container_width=True, key="btn_explain"):
        if check_code(code_input):
            with st.spinner("Preparing explanation..."):
                result = explain_code(code_input, language, explain_level)
            if result:
                save_history("Explain", language, code_input, result)
                st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
                st.markdown(result)

# ── Tab 6: Complexity ──────────────────────────────────────────────────────────
with tabs[5]:
    st.markdown(
        '<p class="fa-icon-label"><i class="fa-solid fa-chart-line"></i> Complexity Analysis</p>',
        unsafe_allow_html=True,
    )
    st.caption("Analyze time complexity, space complexity, and algorithmic patterns.")
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    if st.button("Analyze Complexity", use_container_width=True, key="btn_complexity"):
        if check_code(code_input):
            with st.spinner("Analyzing complexity..."):
                result = complexity_analysis(code_input, language)
            if result:
                save_history("Complexity Analysis", language, code_input, result)
                st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
                st.markdown(result)

# ── Tab 7: Tests ──────────────────────────────────────────────────────────────
with tabs[6]:
    st.markdown(
        '<p class="fa-icon-label"><i class="fa-solid fa-flask-vial"></i> Generate Tests</p>',
        unsafe_allow_html=True,
    )
    test_framework_map = {
        "Python": ["pytest", "unittest", "hypothesis"],
        "JavaScript": ["Jest", "Vitest", "Mocha + Chai"],
        "TypeScript": ["Jest + ts-jest", "Vitest"],
        "Java": ["JUnit 5", "TestNG", "Mockito"],
        "C#": ["xUnit", "NUnit", "MSTest"],
        "Go": ["testing (stdlib)", "testify"],
        "Rust": ["cargo test (built-in)", "proptest"],
    }
    frameworks = test_framework_map.get(language, ["Generic test framework"])
    test_fw = st.selectbox("Testing Framework", frameworks)
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    if st.button("Generate Tests", use_container_width=True, key="btn_tests"):
        if check_code(code_input):
            with st.spinner("Generating test suite..."):
                result = generate_tests(code_input, language, test_fw)
            if result:
                save_history("Generate Tests", language, code_input, result)
                st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
                st.markdown(result)

# ── Tab 8: Translate ──────────────────────────────────────────────────────────
with tabs[7]:
    st.markdown(
        '<p class="fa-icon-label"><i class="fa-solid fa-right-left"></i> Translate Code</p>',
        unsafe_allow_html=True,
    )
    all_langs = ["Python", "JavaScript", "TypeScript", "Java", "C++", "C", "Go",
                 "Rust", "C#", "PHP", "Ruby", "Swift", "Kotlin", "Dart"]
    target_lang = st.selectbox("Translate to", [l for l in all_langs if l != language])
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    if st.button("Translate Code", use_container_width=True, key="btn_translate"):
        if check_code(code_input):
            with st.spinner(f"Translating {language} → {target_lang}..."):
                result = translate_code(code_input, language, target_lang)
            if result:
                save_history(f"Translate → {target_lang}", language, code_input, result)
                st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
                st.markdown(result)

# ── Tab 9: Chat ───────────────────────────────────────────────────────────────
with tabs[8]:
    st.markdown("""
    Ask anything about your code — architecture, specific lines,
    alternatives, bugs, optimizations, or programming concepts.
    """)
    st.markdown("<div style='margin-top: 0.5rem;'></div>", unsafe_allow_html=True)

    USER_AVATAR = "https://api.dicebear.com/7.x/shapes/svg?seed=user&backgroundColor=7c3aed&scale=80"
    BOT_AVATAR  = "https://api.dicebear.com/7.x/shapes/svg?seed=sage&backgroundColor=00d4ff&scale=80"

    for msg in st.session_state.chat_history:
        avatar = USER_AVATAR if msg["role"] == "user" else BOT_AVATAR
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    question = st.chat_input("Ask a question about your code...")

    if question:
        if not code_input.strip():
            st.warning("⚠️ Paste some code first so I have context!")
        else:
            st.session_state.chat_history.append({
                "role": "user",
                "content": question
            })

            with st.chat_message("user", avatar=USER_AVATAR):
                st.markdown(question)

            with st.chat_message("assistant", avatar=BOT_AVATAR):
                with st.spinner("Thinking..."):
                    reply = chat_about_code(
                        code_input,
                        language,
                        question,
                        st.session_state.chat_history[:-1]
                    )
                    if reply:
                        st.markdown(reply)
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": reply
                        })

            st.rerun()

    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2, col3 = st.columns([1, 1, 4])

    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True, key="clear_chat"):
            st.session_state.chat_history = []
            st.rerun()

    with col2:
        st.metric("Messages", len(st.session_state.chat_history))

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
footer()