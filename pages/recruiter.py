import streamlit as st
import os
from dotenv import load_dotenv
from components.styles import MAIN_CSS, DOT_COLORS
from utils.nlp import (
    load_model, extract_text, detect_role_type,
    extract_skills, compute_ats_score, keyword_match_score,
    format_feedback, score_label
)
from utils.llm import get_recruiter_summary

load_dotenv()
BATCH_LIMIT = 10

st.set_page_config(page_title="XreenMe — Recruiter", page_icon="🏢",
                   layout="wide", initial_sidebar_state="collapsed")
st.markdown(MAIN_CSS, unsafe_allow_html=True)

groq_key = st.session_state.get("groq_key", os.getenv("GROQ_API_KEY", ""))

def col(s):  return "#00b884" if s>=75 else ("#f59e0b" if s>=50 else "#ef4444")
def grad(s): return ("linear-gradient(90deg,#00b884,#009e70)" if s>=75
                     else "linear-gradient(90deg,#f59e0b,#d97706)" if s>=50
                     else "linear-gradient(90deg,#ef4444,#dc2626)")

def render_steps(ph, step):
    def d(n):
        c="done" if n<step else ("active" if n==step else "pending")
        return f'<div class="xm-step-dot {c}">{"✓" if n<step else n}</div>'
    def l(n,t):
        c="done" if n<step else ("active" if n==step else "pending")
        return f'<span class="xm-step-label {c}">{t}</span>'
    ph.markdown(f"""<div class="xm-steps">
        <div class="xm-step-item">{d(1)}{l(1,"Upload CVs")}</div>
        <div class="xm-step-line"></div>
        <div class="xm-step-item">{d(2)}{l(2,"Paste JD")}</div>
        <div class="xm-step-line"></div>
        <div class="xm-step-item">{d(3)}{l(3,"Rankings")}</div>
    </div>""", unsafe_allow_html=True)

# Back
cb, _ = st.columns([1,9])
with cb:
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("← Home", key="back_rec"):
        st.session_state.pop("rec_results_ready", None)
        st.switch_page("app.py")
    st.markdown('</div>', unsafe_allow_html=True)

# Header
st.markdown(f"""<div style="margin-bottom:1.8rem;">
    <div class="xm-eyebrow">🏢 Recruiter Mode</div>
    <div style="font-family:'Outfit',sans-serif;font-weight:900;font-size:2.1rem;
    color:#09090f;letter-spacing:-1px;line-height:1.1;margin-bottom:0.4rem;">
        Batch Resume Screener
    </div>
    <div style="color:#7c70a0;font-size:0.88rem;line-height:1.5;">
        Upload up to {BATCH_LIMIT} CVs · Paste one JD · Get ranked candidates instantly
    </div>
</div>""", unsafe_allow_html=True)

_ph = st.empty()
render_steps(_ph, 3 if st.session_state.get("rec_results_ready") else 1)

col_l, col_r = st.columns([1, 1.5], gap="large")

with col_l:
    st.markdown(f'<div style="font-family:\'DM Mono\',monospace;font-size:0.58rem;font-weight:500;'
                f'letter-spacing:3px;text-transform:uppercase;color:#7c70a0;margin-bottom:0.45rem;">'
                f'Step 1 — Upload CVs (Max {BATCH_LIMIT})</div>', unsafe_allow_html=True)

    ufs = st.file_uploader("CVs", type=["pdf","docx","doc"],
                           accept_multiple_files=True,
                           label_visibility="collapsed", key="rec_uploader")
    if ufs and len(ufs) > BATCH_LIMIT:
        st.warning(f"⚠️ Max {BATCH_LIMIT} — only first {BATCH_LIMIT} used.")
        ufs = ufs[:BATCH_LIMIT]

    n = len(ufs) if ufs else 0

    if ufs:
        render_steps(_ph, 2)
        for f in ufs:
            sz = round(f.size/1024, 1)
            st.markdown(f"""<div class="xm-file-pill">
                <span style="font-size:0.81rem;font-weight:600;color:#006b4e;">✅ {f.name}</span>
                <span style="font-size:0.7rem;color:#7c70a0;font-family:'DM Mono',monospace;">{sz} KB</span>
            </div>""", unsafe_allow_html=True)
        st.markdown(f'<div style="font-family:\'DM Mono\',monospace;font-size:0.7rem;color:#7c70a0;'
                    f'margin-top:7px;">{n} CV{"s" if n!=1 else ""} ready to screen</div>',
                    unsafe_allow_html=True)

    st.markdown("<div style='height:0.9rem;'></div>", unsafe_allow_html=True)
    st.markdown('<div style="font-family:\'DM Mono\',monospace;font-size:0.58rem;font-weight:500;'
                'letter-spacing:3px;text-transform:uppercase;color:#7c70a0;margin-bottom:0.45rem;">'
                'Step 2 — Paste Job Description</div>', unsafe_allow_html=True)

    jd = st.text_area("JD", height=185,
                      placeholder="Paste the full JD for the role you're hiring...",
                      label_visibility="collapsed", key="rec_jd")

    st.markdown("<div style='height:0.7rem;'></div>", unsafe_allow_html=True)
    btn_lbl = f"🏆 Rank {n} Candidate{'s' if n!=1 else ''}" if n>0 else "🏆 Rank Candidates"
    run = st.button(btn_lbl, use_container_width=True, key="screen_btn")

    with col_r:
        if not st.session_state.get("rec_results_ready") and not run:
            st.markdown("""<div style="text-align:center;padding:6rem 2rem;">
                <div style="font-size:2.8rem;opacity:0.1;margin-bottom:1rem;">🏢</div>
                <div style="font-family:'DM Mono',monospace;font-size:0.6rem;letter-spacing:4px;
                text-transform:uppercase;color:#cec6e8;line-height:3;">
                    Upload CVs · Paste a JD · Click Rank
                </div></div>""", unsafe_allow_html=True)

if not run:
    st.stop()

if not ufs:
    st.error("⚠️ Please upload at least one CV."); st.stop()
if not jd.strip():
    st.error("⚠️ Please paste the job description."); st.stop()

with st.spinner("Screening all candidates..."):
    model    = load_model()
    rtype    = detect_role_type(jd)
    results  = []
    for f in ufs:
        rtext = extract_text(f)
        if not rtext: continue
        overall, secs = compute_ats_score(model, rtext, jd)
        kw_s,_,_,_   = keyword_match_score(rtext, jd)
        jdsk          = set(extract_skills(jd, rtype))
        resk          = set(extract_skills(rtext, rtype))
        mtch          = sorted(jdsk & resk)
        miss          = sorted(jdsk - resk)
        fmt           = format_feedback(rtext)
        note = ""
        if groq_key:
            note = get_recruiter_summary(rtext, jd, overall, mtch, miss, rtype, groq_key)
        results.append({"name":f.name.rsplit(".",1)[0], "score":overall,
                        "kw":kw_s, "secs":secs, "matched":mtch,
                        "missing":miss, "fmt":fmt, "note":note})

results.sort(key=lambda x: x["score"], reverse=True)
st.session_state["rec_results_ready"] = True
render_steps(_ph, 3)

with col_r:
    rcls = "tag-tech" if rtype=="tech" else "tag-ntech"
    rico = "⚙️ Technical Role" if rtype=="tech" else "💼 Non-Technical Role"

    st.markdown(f"""<div style="display:flex;align-items:center;gap:10px;margin-bottom:1.2rem;">
        <span class="xm-tag {rcls}">{rico}</span>
        <span style="font-size:0.76rem;color:#7c70a0;font-family:'DM Mono',monospace;">
            {len(results)} candidate{"s" if len(results)!=1 else ""} ranked
        </span>
    </div>
    <div style="font-family:'DM Mono',monospace;font-size:0.56rem;font-weight:500;
    letter-spacing:4px;text-transform:uppercase;color:#7c70a0;
    padding-bottom:0.75rem;border-bottom:1.5px solid #e8e4f3;margin-bottom:1rem;">
        Candidate Rankings
    </div>""", unsafe_allow_html=True)

    for i, r in enumerate(results):
        medal = ["🥇","🥈","🥉"][i] if i<3 else f"#{i+1}"
        sc_col = col(r["score"])
        kw_col = col(r["kw"])

        # ── Rank card — build matched tags separately to avoid nested f-string bug ──
        matched_tags = "".join(f'<span class="xm-tag tag-match">{s}</span>'
                               for s in r["matched"][:5])

        st.markdown(f"""<div class="xm-rank-card">
            <div class="xm-rank-medal">{medal}</div>
            <div style="flex:1;min-width:0;">
                <div class="xm-rank-name">{r["name"]}</div>
                <div class="xm-rank-detail">{score_label(r["score"])}</div>
                <div class="xm-rank-scores">
                    <div class="xm-rank-score-item">
                        <span class="xm-rank-score-label">🧠 Semantic</span>
                        <span class="xm-rank-score-val" style="color:{sc_col};">{r["score"]}%</span>
                    </div>
                    <div class="xm-rank-score-item">
                        <span class="xm-rank-score-label">🔍 Keyword</span>
                        <span class="xm-rank-score-val" style="color:{kw_col};">{r["kw"]}%</span>
                    </div>
                </div>
                <div>{matched_tags}</div>
            </div>
        </div>""", unsafe_allow_html=True)

        if r["note"]:
            st.markdown(f'<div class="xm-ai-note">🤖 {r["note"]}</div>',
                        unsafe_allow_html=True)

        with st.expander(f"📋 Full breakdown — {r['name']}"):
            desired = ["Experience","Skills","Education","Projects"]
            ordered = {k: r["secs"][k] for k in desired if k in r["secs"]}
            for k,v in r["secs"].items():
                if k not in ordered: ordered[k]=v

            bl, br = st.columns(2, gap="large")
            for j,(sec,val) in enumerate(ordered.items()):
                with (bl if j%2==0 else br):
                    st.markdown(f"""<div class="xm-bar-wrap">
                        <div class="xm-bar-meta"><span>{sec}</span>
                        <span style="color:{col(val)};font-weight:800;">{val}%</span></div>
                        <div class="xm-bar-track">
                            <div class="xm-bar-fill" style="width:{val}%;background:{grad(val)};"></div>
                        </div>
                    </div>""", unsafe_allow_html=True)

            if r["missing"]:
                miss_tags = "".join(f'<span class="xm-tag tag-miss">{s}</span>'
                                    for s in r["missing"])
                st.markdown(f'<div style="margin:10px 0 5px;font-size:0.78rem;font-weight:600;'
                            f'color:#b91c1c;">❌ Missing Skills</div>{miss_tags}',
                            unsafe_allow_html=True)

            st.markdown('<div style="margin:12px 0 6px;font-size:0.75rem;font-weight:600;'
                        'color:#7c70a0;">📋 Format Check</div>', unsafe_allow_html=True)
            for lv,msg in r["fmt"]:
                st.markdown(f"""<div class="xm-fmt-row">
                    <div class="xm-fmt-dot" style="background:{DOT_COLORS[lv]};"></div>
                    <span>{msg}</span>
                </div>""", unsafe_allow_html=True)

    if not groq_key:
        st.markdown('<div class="xm-api-nudge" style="margin-top:1rem;">'
                    '🔑 Add your Groq API key in the sidebar for AI hiring recommendations.'
                    '</div>', unsafe_allow_html=True)