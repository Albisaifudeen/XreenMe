import streamlit as st
import os
from dotenv import load_dotenv
from components.styles import MAIN_CSS
from utils.llm import LANDING_QUOTE

load_dotenv()

st.set_page_config(
    page_title="XreenMe — AI Resume Screener",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown(MAIN_CSS, unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
env_key = os.getenv("GROQ_API_KEY", "")
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    manual_key = st.text_input("Groq API Key", type="password",
        placeholder="gsk_...", value="")
    groq_key = manual_key if manual_key else env_key
    if groq_key:
        st.success("✅ API key active")
    else:
        st.warning("⚠️ No key — basic mode")
    st.markdown("---")
    st.markdown("🔒 Resumes processed in memory only.")
    st.markdown("---")
    st.markdown("**Free Groq key:**")
    st.markdown("→ [console.groq.com](https://console.groq.com)")

st.session_state["groq_key"] = groq_key

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="xm-hero">
    <div class="xm-eyebrow">⚡ AI-Powered Resume Screening</div>
    <div class="xm-hero-title">Xreen<span>Me</span></div>
    <div class="xm-hero-sub">
        Beyond keyword matching — semantic AI that understands your resume
        the way a recruiter actually reads it.
    </div>
    <div class="xm-hero-quote">✦ {LANDING_QUOTE}</div>
</div>
""", unsafe_allow_html=True)

# ── Mode label ────────────────────────────────────────────────────────────────
st.markdown("""
<div style="font-family:'DM Mono',monospace;font-size:0.6rem;font-weight:500;
letter-spacing:5px;text-transform:uppercase;color:#6b5f8a;
margin-bottom:1.3rem;">Choose Your Mode</div>
""", unsafe_allow_html=True)

# ── Mode cards ────────────────────────────────────────────────────────────────
col_ind, col_rec = st.columns(2, gap="large")

with col_ind:
    st.markdown("""
    <div class="xm-mode-card">
        <div class="xm-mode-icon">👤</div>
        <div class="xm-mode-title">Individual Mode</div>
        <div class="xm-mode-sub">Check your own CV against a job description</div>
        <div class="xm-mode-feat"><span class="xm-feat-dot">◆</span><span>Dual scoring — Semantic ATS + Keyword Match</span></div>
        <div class="xm-mode-feat"><span class="xm-feat-dot">◆</span><span>Section breakdown — Experience, Skills, Education, Projects</span></div>
        <div class="xm-mode-feat"><span class="xm-feat-dot">◆</span><span>Missing experience keywords highlighted</span></div>
        <div class="xm-mode-feat"><span class="xm-feat-dot">◆</span><span>Skill gap — matched vs missing from JD</span></div>
        <div class="xm-mode-feat"><span class="xm-feat-dot">◆</span><span>Resume format check </span></div>
        <div class="xm-mode-feat"><span class="xm-feat-dot">◆</span><span>🤖 AI coach tips + interview questions <em style="color:#6b5f8a;">(API)</em></span></div>
    </div>
    """, unsafe_allow_html=True)
    ind_btn = st.button("→ Start Individual Check", key="ind_mode")

with col_rec:
    st.markdown("""
    <div class="xm-mode-card">
        <div class="xm-mode-icon">🏢</div>
        <div class="xm-mode-title">Recruiter Mode</div>
        <div class="xm-mode-sub">Screen and rank up to 10 resumes at once</div>
        <div class="xm-mode-feat"><span class="xm-feat-dot">◆</span><span>Batch process up to <strong>10 CVs</strong> simultaneously</span></div>
        <div class="xm-mode-feat"><span class="xm-feat-dot">◆</span><span>Ranked by ATS score — 🥇🥈🥉 medals</span></div>
        <div class="xm-mode-feat"><span class="xm-feat-dot">◆</span><span>Dual scores per candidate (Semantic + Keyword)</span></div>
        <div class="xm-mode-feat"><span class="xm-feat-dot">◆</span><span>Full per-candidate breakdown — expandable</span></div>
        <div class="xm-mode-feat"><span class="xm-feat-dot">◆</span><span>Tech vs Non-Tech role auto-detection</span></div>
        <div class="xm-mode-feat"><span class="xm-feat-dot">◆</span><span>🤖 AI hiring recommendation per candidate <em style="color:#6b5f8a;">(API)</em></span></div>
    </div>
    """, unsafe_allow_html=True)
    rec_btn = st.button("→ Start Recruiter Screening", key="rec_mode")

if ind_btn: st.switch_page("pages/individual.py")
if rec_btn: st.switch_page("pages/recruiter.py")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:3.5rem;padding-top:1.5rem;
border-top:1.5px solid #e2dcf5;color:#6b5f8a;font-size:0.75rem;
font-family:'DM Mono',monospace;letter-spacing:1px;line-height:2.2;">
    🔒 Your data never leaves this session &nbsp;·&nbsp;
    SBERT + Groq LLaMA3 &nbsp;·&nbsp;
    XreenMe © 2026
</div>
""", unsafe_allow_html=True)