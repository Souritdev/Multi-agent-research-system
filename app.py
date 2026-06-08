import streamlit as st

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Session state init ────────────────────────────────────────────────────────
if "step_states" not in st.session_state:
    st.session_state.step_states = ["idle"] * 4
if "pipeline_result" not in st.session_state:
    st.session_state.pipeline_result = None
if "error_msg" not in st.session_state:
    st.session_state.error_msg = None
if "current_topic" not in st.session_state:
    st.session_state.current_topic = ""
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False   # default = light / day mode

dark = st.session_state.dark_mode

# ── Theme tokens ─────────────────────────────────────────────────────────────
if dark:
    BG            = "#0a0a0f"
    BG_GRAD       = "radial-gradient(ellipse 80% 50% at 20% -10%, rgba(99,57,255,0.18) 0%, transparent 60%), radial-gradient(ellipse 60% 40% at 80% 110%, rgba(0,210,180,0.12) 0%, transparent 55%)"
    TEXT_PRI      = "#e8e0ff"
    TEXT_SEC      = "#9ca3af"
    TEXT_MUT      = "#4b5563"
    BORDER        = "rgba(255,255,255,0.07)"
    CARD_BG       = "rgba(255,255,255,0.025)"
    INPUT_BG      = "rgba(255,255,255,0.04)"
    INPUT_BDR     = "rgba(167,139,250,0.25)"
    INPUT_CLR     = "#e8e0ff"
    HERO_GRAD     = "linear-gradient(135deg, #e8e0ff 0%, #a78bfa 45%, #34d399 100%)"
    STEP_DONE_BDR = "rgba(52,211,153,0.45)"
    STEP_DONE_BG  = "rgba(52,211,153,0.05)"
    STEP_IDLE_BDR = "rgba(255,255,255,0.07)"
    STEP_IDLE_BG  = "rgba(255,255,255,0.025)"
    HR_CLR        = "rgba(255,255,255,0.05)"
    PANEL_HDG     = "#4b5563"
    TOGGLE_BG     = "rgba(255,255,255,0.06)"
    TOGGLE_CLR    = "#9ca3af"
    TOGGLE_ICON   = "☀️"
    RPT_BG        = "rgba(255,255,255,0.02)"
    RPT_BDR       = "rgba(255,255,255,0.06)"
    RPT_H_CLR     = "#e8e0ff"
    RPT_P_CLR     = "#c4b5fd"
    FOOT_CLR      = "#1f2937"
    DL_BG         = "rgba(255,255,255,0.04)"
    DL_BDR        = "rgba(255,255,255,0.1)"
    DL_CLR        = "#9ca3af"
    DL_HBG        = "rgba(167,139,250,0.08)"
    DL_HBDR       = "rgba(167,139,250,0.35)"
    DL_HCLR       = "#a78bfa"
    SHADOW        = "0.15"
    ERR_BG        = "rgba(239,68,68,0.05)"
else:
    BG            = "#f5f4f0"
    BG_GRAD       = "radial-gradient(ellipse 80% 50% at 20% -10%, rgba(167,139,250,0.10) 0%, transparent 60%), radial-gradient(ellipse 60% 40% at 80% 110%, rgba(52,211,153,0.08) 0%, transparent 55%)"
    TEXT_PRI      = "#1a1523"
    TEXT_SEC      = "#374151"
    TEXT_MUT      = "#6b7280"
    BORDER        = "rgba(0,0,0,0.09)"
    CARD_BG       = "#ffffff"
    INPUT_BG      = "#ffffff"
    INPUT_BDR     = "rgba(124,58,237,0.3)"
    INPUT_CLR     = "#1a1523"
    HERO_GRAD     = "linear-gradient(135deg, #4f46e5 0%, #7c3aed 45%, #059669 100%)"
    STEP_DONE_BDR = "rgba(5,150,105,0.5)"
    STEP_DONE_BG  = "rgba(5,150,105,0.06)"
    STEP_IDLE_BDR = "rgba(0,0,0,0.09)"
    STEP_IDLE_BG  = "#ffffff"
    HR_CLR        = "rgba(0,0,0,0.08)"
    PANEL_HDG     = "#6b7280"
    TOGGLE_BG     = "rgba(0,0,0,0.06)"
    TOGGLE_CLR    = "#374151"
    TOGGLE_ICON   = "🌙"
    RPT_BG        = "#ffffff"
    RPT_BDR       = "rgba(0,0,0,0.08)"
    RPT_H_CLR     = "#1a1523"
    RPT_P_CLR     = "#374151"
    FOOT_CLR      = "#9ca3af"
    DL_BG         = "#ffffff"
    DL_BDR        = "rgba(0,0,0,0.12)"
    DL_CLR        = "#374151"
    DL_HBG        = "rgba(124,58,237,0.06)"
    DL_HBDR       = "rgba(124,58,237,0.3)"
    DL_HCLR       = "#7c3aed"
    SHADOW        = "0.06"
    ERR_BG        = "rgba(239,68,68,0.04)"

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=Lora:ital,wght@0,400;0,600;1,400&display=swap');

html, body, [class*="css"] {{ font-family: 'DM Mono', monospace; }}

.stApp {{
    background: {BG};
    background-image: {BG_GRAD};
    transition: background 0.35s ease;
}}

#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding-top: 2rem; padding-bottom: 3rem; max-width: 1400px; }}

/* ── Hero ── */
.hero-wrap {{ text-align: center; padding: 0.8rem 0 1.8rem; }}
.hero-title {{
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: clamp(2.2rem, 5.5vw, 3.8rem);
    letter-spacing: -0.03em;
    line-height: 1.05;
    background: {HERO_GRAD};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.4rem;
}}
.hero-sub {{
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: {TEXT_MUT};
    letter-spacing: 0.2em;
    text-transform: uppercase;
}}

/* ── Input ── */
.stTextInput > div > div > input {{
    background: {INPUT_BG} !important;
    border: 1px solid {INPUT_BDR} !important;
    border-radius: 10px !important;
    color: {INPUT_CLR} !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.95rem !important;
    padding: 0.85rem 1.2rem !important;
    caret-color: #7c3aed;
    transition: border-color 0.2s, box-shadow 0.2s;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}}
.stTextInput > div > div > input:focus {{
    border-color: rgba(124,58,237,0.6) !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.1) !important;
}}
.stTextInput > div > div > input::placeholder {{ color: {TEXT_MUT} !important; }}
.stTextInput label {{ display: none !important; }}

/* ── Buttons (Run + Toggle share base) ── */
.stButton > button {{
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    border: none !important;
    border-radius: 10px !important;
    color: #fff !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.92rem !important;
    letter-spacing: 0.04em;
    padding: 0.78rem 1.4rem !important;
    transition: opacity 0.2s, transform 0.15s, box-shadow 0.2s !important;
    box-shadow: 0 4px 18px rgba(124,58,237,0.35) !important;
    width: 100%;
}}
.stButton > button:hover {{
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 24px rgba(124,58,237,0.5) !important;
}}
.stButton > button:active {{ transform: translateY(0) !important; }}

/* Override toggle button to look pill-shaped and subtle */
[data-testid="stButton"][key="theme_toggle"] > button,
div[data-testid="column"]:last-child .stButton > button {{
    background: {TOGGLE_BG} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 999px !important;
    color: {TOGGLE_CLR} !important;
    font-family: 'DM Mono', monospace !important;
    font-weight: 400 !important;
    font-size: 0.75rem !important;
    box-shadow: none !important;
    padding: 0.4rem 1rem !important;
}}

/* ── Panel heading ── */
.panel-heading {{
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: {PANEL_HDG};
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid {HR_CLR};
}}

/* ── Step cards ── */
.step-card {{
    background: {STEP_IDLE_BG};
    border: 1px solid {STEP_IDLE_BDR};
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.85rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}}
.step-card.done {{
    border-color: {STEP_DONE_BDR};
    background: {STEP_DONE_BG};
}}
.step-card.error {{
    border-color: rgba(239,68,68,0.45);
    background: {ERR_BG};
}}
.step-header {{
    display: flex;
    align-items: center;
    gap: 0.55rem;
    margin-bottom: 0.3rem;
}}
.step-num {{
    font-family: 'DM Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.15em;
    color: {TEXT_MUT};
    text-transform: uppercase;
    flex-shrink: 0;
}}
.step-label {{
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.9rem;
    color: {TEXT_PRI};
}}
.step-status {{
    margin-left: auto;
    font-size: 0.95rem;
    flex-shrink: 0;
}}
.step-status.idle  {{ color: {TEXT_MUT}; }}
.step-status.done  {{ color: #10b981; }}
.step-status.error {{ color: #ef4444; }}
.step-desc {{
    font-size: 0.72rem;
    color: {TEXT_MUT};
    line-height: 1.5;
}}

/* ── Report wrap ── */
.report-wrap {{
    background: {RPT_BG};
    border: 1px solid {RPT_BDR};
    border-radius: 14px;
    padding: 2rem 2.4rem;
    box-shadow: 0 2px 12px rgba(0,0,0,{SHADOW});
}}
.report-wrap h1, .report-wrap h2, .report-wrap h3 {{
    font-family: 'Syne', sans-serif !important;
    color: {RPT_H_CLR} !important;
    margin-top: 1.4rem !important;
    font-weight: 700 !important;
}}
.report-wrap h1 {{ font-size: 1.6rem !important; margin-top: 0 !important; }}
.report-wrap h2 {{ font-size: 1.2rem !important; }}
.report-wrap h3 {{ font-size: 1rem !important; }}
.report-wrap p, .report-wrap li {{
    font-family: 'Lora', serif !important;
    color: {RPT_P_CLR} !important;
    font-size: 0.95rem !important;
    line-height: 1.8 !important;
}}
.report-wrap strong {{ color: {RPT_H_CLR} !important; }}
.report-wrap hr {{ border-color: {HR_CLR} !important; margin: 1.2rem 0 !important; }}

/* ── Section label ── */
.section-label {{
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: {PANEL_HDG};
    margin-bottom: 0.7rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}
.badge {{
    display: inline-flex;
    align-items: center;
    padding: 0.12rem 0.5rem;
    border-radius: 999px;
    font-size: 0.58rem;
    font-family: 'DM Mono', monospace;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}}
.badge-green {{ background: rgba(16,185,129,0.12); color: #10b981; }}
.badge-amber {{ background: rgba(245,158,11,0.12);  color: #f59e0b; }}
.badge-red   {{ background: rgba(239,68,68,0.12);   color: #ef4444; }}

/* ── Idle placeholder ── */
.idle-box {{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.9rem;
    height: 360px;
    border: 1.5px dashed {BORDER};
    border-radius: 14px;
    background: {CARD_BG};
}}
.idle-icon {{ font-size: 2.5rem; opacity: 0.18; }}
.idle-text {{
    color: {TEXT_MUT};
    font-size: 0.72rem;
    font-family: 'DM Mono', monospace;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}}

/* ── Misc ── */
hr {{ border-color: {HR_CLR} !important; margin: 1.4rem 0 !important; }}
.stSpinner > div {{ border-top-color: #7c3aed !important; }}
.stAlert {{ border-radius: 10px !important; }}
.streamlit-expanderHeader {{
    background: {CARD_BG} !important;
    border-radius: 8px !important;
    color: {TEXT_MUT} !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    border: 1px solid {BORDER} !important;
}}
.stDownloadButton > button {{
    background: {DL_BG} !important;
    border: 1px solid {DL_BDR} !important;
    border-radius: 8px !important;
    color: {DL_CLR} !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    transition: background 0.2s, border-color 0.2s !important;
}}
.stDownloadButton > button:hover {{
    background: {DL_HBG} !important;
    border-color: {DL_HBDR} !important;
    color: {DL_HCLR} !important;
}}
</style>
""", unsafe_allow_html=True)

# ── Theme toggle (top-right) ──────────────────────────────────────────────────
t1, t2, t3 = st.columns([8, 1, 1])
with t3:
    if st.button(f"{TOGGLE_ICON} {'Dark' if not dark else 'Light'}", key="theme_toggle"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-title">Multi-Agent Research</div>
    <div class="hero-sub">Search &nbsp;·&nbsp; Scrape &nbsp;·&nbsp; Write &nbsp;·&nbsp; Critique</div>
</div>
""", unsafe_allow_html=True)

# ── Input bar ─────────────────────────────────────────────────────────────────
inp_col, btn_col = st.columns([5, 1], gap="small")
with inp_col:
    topic = st.text_input(
        "topic",
        placeholder="e.g. The future of autonomous AI agents …",
        label_visibility="collapsed",
    )
with btn_col:
    run_btn = st.button("▶ Run Research", use_container_width=True)

st.markdown("<div style='margin-bottom:1.6rem'></div>", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────────────────
STEPS = [
    ("01", "Search Agent",  "Queries the web for recent, reliable information on the topic."),
    ("02", "Reader Agent",  "Picks the top URL from search results and deep-scrapes its content."),
    ("03", "Writer Chain",  "Synthesises search + scraped content into a structured report."),
    ("04", "Critic Chain",  "Reviews the report for accuracy, depth, and improvements."),
]
STATUS_ICON  = {"idle": "○", "done": "✓", "error": "✗"}
STATUS_CLASS = {"idle": "idle", "done": "done", "error": "error"}

# ── Two-column layout: REPORT LEFT · PIPELINE RIGHT ──────────────────────────
report_col, pipeline_col = st.columns([2, 1], gap="large")

# ── Helper: render final pipeline cards (only called after full run) ──────────
def render_final_steps():
    with pipeline_col:
        st.markdown('<div class="panel-heading">Pipeline Status</div>', unsafe_allow_html=True)
        for i, (num, label, desc) in enumerate(STEPS):
            s   = st.session_state.step_states[i]
            cls  = STATUS_CLASS.get(s, "idle")
            icon = STATUS_ICON.get(s, "○")
            st.markdown(f"""
            <div class="step-card {cls}">
                <div class="step-header">
                    <span class="step-num">#{num}</span>
                    <span class="step-label">{label}</span>
                    <span class="step-status {cls}">{icon}</span>
                </div>
                <div class="step-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

# ── Idle placeholders ─────────────────────────────────────────────────────────
with report_col:
    st.markdown('<div class="panel-heading">Research Output</div>', unsafe_allow_html=True)
    if not run_btn and st.session_state.pipeline_result is None and st.session_state.error_msg is None:
        st.markdown("""
        <div class="idle-box">
            <div class="idle-icon">🔬</div>
            <div class="idle-text">Enter a topic and click Run Research</div>
        </div>
        """, unsafe_allow_html=True)

with pipeline_col:
    if not run_btn and st.session_state.pipeline_result is None and st.session_state.error_msg is None:
        st.markdown('<div class="panel-heading">Pipeline Status</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="idle-box" style="height:260px;">
            <div class="idle-icon">⚙️</div>
            <div class="idle-text">Waiting to start</div>
        </div>
        """, unsafe_allow_html=True)

# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        with report_col:
            st.warning("Please enter a research topic first.")
    else:
        st.session_state.step_states     = ["idle"] * 4
        st.session_state.pipeline_result = None
        st.session_state.error_msg       = None
        st.session_state.current_topic   = topic

        with report_col:
            st.markdown('<div class="panel-heading">Research Output</div>', unsafe_allow_html=True)

        with pipeline_col:
            st.markdown('<div class="panel-heading">Pipeline Status</div>', unsafe_allow_html=True)
            running_box = st.empty()
            running_box.markdown("""
            <div class="idle-box" style="height:260px;">
                <div class="idle-icon" style="opacity:0.4;animation:spin 1.5s linear infinite;">⚙️</div>
                <div class="idle-text">Pipeline running…</div>
            </div>
            <style>
            @keyframes spin { from{transform:rotate(0deg)} to{transform:rotate(360deg)} }
            </style>
            """, unsafe_allow_html=True)

        try:
            from agents import build_search_agent, build_reader_agent, critic_chain, writer_chain
            state = {}

            # Step 1 — Search
            with report_col:
                with st.spinner("🔍 Search Agent is querying the web…"):
                    search_agent  = build_search_agent()
                    search_result = search_agent.invoke({
                        "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
                    })
                    state["search_results"] = search_result["messages"][-1].content
            st.session_state.step_states[0] = "done"

            # Step 2 — Reader
            with report_col:
                with st.spinner("📰 Reader Agent is scraping top resource…"):
                    reader_agent  = build_reader_agent()
                    reader_result = reader_agent.invoke({
                        "messages": [("user",
                            f"Based on the following search results about '{topic}', "
                            f"pick the most relevant URL and scrape it for deeper content.\n\n"
                            f"Search Results:\n{state['search_results'][:800]}"
                        )]
                    })
                    state["scraped_content"] = reader_result["messages"][-1].content
            st.session_state.step_states[1] = "done"

            # Step 3 — Writer
            with report_col:
                with st.spinner("✍️ Writer Chain is drafting the report…"):
                    research_combined = (
                        f"SEARCH RESULTS:\n{state['search_results']}\n\n"
                        f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}\n\n"
                    )
                    state["report"] = writer_chain.invoke({
                        "topic": topic,
                        "research": research_combined
                    })
            st.session_state.step_states[2] = "done"

            # Step 4 — Critic
            with report_col:
                with st.spinner("🧐 Critic Chain is reviewing the report…"):
                    state["feedback"] = critic_chain.invoke({
                        "report": state["report"]
                    })
            st.session_state.step_states[3] = "done"

            running_box.empty()
            st.session_state.pipeline_result = state

        except Exception as e:
            for i in range(4):
                if st.session_state.step_states[i] == "idle":
                    st.session_state.step_states[i] = "error"
                    break
            running_box.empty()
            st.session_state.error_msg = str(e)

        st.rerun()

# ── Show final pipeline cards (only after run completes) ─────────────────────
if st.session_state.pipeline_result is not None or st.session_state.error_msg is not None:
    render_final_steps()

# ── Display results in report_col ─────────────────────────────────────────────
with report_col:
    err         = st.session_state.error_msg
    result      = st.session_state.pipeline_result
    saved_topic = st.session_state.current_topic

    if err:
        st.markdown(f"""
        <div class="section-label">⚠ Pipeline Error <span class="badge badge-red">failed</span></div>
        <div class="report-wrap" style="border-color:rgba(239,68,68,0.25);">
            <p style="color:#ef4444;">{err}</p>
        </div>
        """, unsafe_allow_html=True)

    if result:
        # Final Report
        st.markdown("""
        <div class="section-label">
            📄 Final Report <span class="badge badge-green">done</span>
        </div>
        """, unsafe_allow_html=True)

        report_text = result.get("report", "")
        if isinstance(report_text, dict):
            report_text = str(report_text)

        st.markdown('<div class="report-wrap">', unsafe_allow_html=True)
        st.markdown(report_text)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<div style='margin-top:1.6rem'></div>", unsafe_allow_html=True)

        # Critic Feedback
        st.markdown("""
        <div class="section-label">
            🧐 Critic Feedback <span class="badge badge-amber">review</span>
        </div>
        """, unsafe_allow_html=True)

        feedback_text = result.get("feedback", "")
        if isinstance(feedback_text, dict):
            feedback_text = str(feedback_text)

        st.markdown('<div class="report-wrap">', unsafe_allow_html=True)
        st.markdown(feedback_text)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<div style='margin-top:1.6rem'></div>", unsafe_allow_html=True)

        # Raw expanders
        with st.expander("🔍 Raw Search Results"):
            st.text(result.get("search_results", ""))
        with st.expander("📰 Raw Scraped Content"):
            st.text(result.get("scraped_content", ""))

        st.markdown("<div style='margin-top:1.2rem'></div>", unsafe_allow_html=True)

        # Downloads
        dl1, dl2 = st.columns(2)
        safe = saved_topic[:30].replace(" ", "_")
        with dl1:
            st.download_button(
                label="⬇ Download Report",
                data=str(result.get("report", "")),
                file_name=f"report_{safe}.txt",
                mime="text/plain",
                use_container_width=True,
            )
        with dl2:
            st.download_button(
                label="⬇ Download Feedback",
                data=str(result.get("feedback", "")),
                file_name=f"feedback_{safe}.txt",
                mime="text/plain",
                use_container_width=True,
            )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<p style="text-align:center; color:{FOOT_CLR}; font-size:0.65rem;
   font-family:'DM Mono',monospace; letter-spacing:0.14em;
   text-transform:uppercase; margin-top:3rem;">
    Multi-Agent Research System &nbsp;·&nbsp; Powered by LangChain
</p>
""", unsafe_allow_html=True)