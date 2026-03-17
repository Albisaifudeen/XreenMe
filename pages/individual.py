import streamlit as st
import os
import re as _re
from dotenv import load_dotenv
from components.styles import MAIN_CSS, DOT_COLORS
from utils.nlp import (
    load_model, extract_text, detect_role_type,
    extract_skills, compute_ats_score, keyword_match_score,
    format_feedback, score_label
)
from utils.llm import get_career_coach, parse_coach_output, score_quote

load_dotenv()

st.set_page_config(page_title="XreenMe — Individual", page_icon="👤",
                   layout="wide", initial_sidebar_state="collapsed")
st.markdown(MAIN_CSS, unsafe_allow_html=True)

groq_key = st.session_state.get("groq_key", os.getenv("GROQ_API_KEY", ""))

def col(s):
    return "#00b884" if s >= 75 else ("#f59e0b" if s >= 50 else "#ef4444")

def grad(s):
    return ("linear-gradient(90deg,#00b884,#009e70)" if s >= 75
            else "linear-gradient(90deg,#f59e0b,#d97706)" if s >= 50
            else "linear-gradient(90deg,#ef4444,#dc2626)")

def render_steps(ph, step):
    def d(n):
        c = "done" if n < step else ("active" if n == step else "pending")
        return f'<div class="xm-step-dot {c}">{"✓" if n < step else n}</div>'
    def l(n, t):
        c = "done" if n < step else ("active" if n == step else "pending")
        return f'<span class="xm-step-label {c}">{t}</span>'
    ph.markdown(f"""<div class="xm-steps">
        <div class="xm-step-item">{d(1)}{l(1,"Upload CV")}</div>
        <div class="xm-step-line"></div>
        <div class="xm-step-item">{d(2)}{l(2,"Paste JD")}</div>
        <div class="xm-step-line"></div>
        <div class="xm-step-item">{d(3)}{l(3,"Results")}</div>
    </div>""", unsafe_allow_html=True)

# Back
cb, _ = st.columns([1, 9])
with cb:
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("← Home", key="back_ind"):
        for k in ["results_ready","_has_cv","_has_jd","_uploaded_file"]:
            st.session_state.pop(k, None)
        st.switch_page("app.py")
    st.markdown('</div>', unsafe_allow_html=True)

# Header
st.markdown("""
<div style="margin-bottom:1.8rem;">
    <div class="xm-eyebrow">👤 Individual Mode</div>
    <div style="font-family:'Outfit',sans-serif;font-weight:900;font-size:2.1rem;
    color:#09090f;letter-spacing:-1px;line-height:1.1;margin-bottom:0.4rem;">
        Resume Score Checker
    </div>
    <div style="color:#7c70a0;font-size:0.88rem;line-height:1.5;">
        Upload your CV · Paste a JD · Get a full breakdown instantly
    </div>
</div>""", unsafe_allow_html=True)

# Step bar
_ph = st.empty()
render_steps(_ph, 3 if st.session_state.get("results_ready") else
             (2 if st.session_state.get("_has_cv") else 1))

# Inputs
cu, cj = st.columns(2, gap="large")
with cu:
    st.markdown('<div style="font-family:\'DM Mono\',monospace;font-size:0.58rem;font-weight:500;'
                'letter-spacing:3px;text-transform:uppercase;color:#7c70a0;margin-bottom:0.45rem;">'
                'Step 1 — Upload Your CV</div>', unsafe_allow_html=True)
    uf = st.file_uploader("CV", type=["pdf","docx","doc"],
                          label_visibility="collapsed", key="cv_uploader")
    if uf:
        st.session_state["_has_cv"] = True
        st.session_state["_uploaded_file"] = uf
        render_steps(_ph, 2)

with cj:
    st.markdown('<div style="font-family:\'DM Mono\',monospace;font-size:0.58rem;font-weight:500;'
                'letter-spacing:3px;text-transform:uppercase;color:#7c70a0;margin-bottom:0.45rem;">'
                'Step 2 — Paste Job Description</div>', unsafe_allow_html=True)
    jd = st.text_area("JD", height=155,
                      placeholder="Copy the full JD from LinkedIn, Naukri, Indeed...",
                      label_visibility="collapsed", key="jd_text")
    st.session_state["_has_jd"] = bool(jd and jd.strip())

st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
_, bc, _ = st.columns([1,2,1])
with bc:
    run = st.button("⚡ Analyse My Resume", use_container_width=True)

st.markdown('<hr class="xm-divider">', unsafe_allow_html=True)

if not run:
    if not st.session_state.get("results_ready"):
        st.markdown("""<div style="text-align:center;padding:5rem 2rem;">
            <div style="font-size:2.8rem;opacity:0.12;margin-bottom:1rem;">👤</div>
            <div style="font-family:'DM Mono',monospace;font-size:0.6rem;letter-spacing:4px;
            text-transform:uppercase;color:#cec6e8;line-height:3;">
                Upload your CV · Paste a JD · Click Analyse
            </div></div>""", unsafe_allow_html=True)
    st.stop()

# ── Run analysis ──────────────────────────────────────────────────────────────
cv = uf or st.session_state.get("_uploaded_file")
if not cv:
    st.error("⚠️ Please upload your CV first."); st.stop()
if not jd.strip():
    st.error("⚠️ Please paste the job description."); st.stop()

with st.spinner("Analysing your resume..."):
    model  = load_model()
    rtext  = extract_text(cv)
    if not rtext:
        st.error("Could not read file. Use a text-based PDF or Word doc."); st.stop()

    rtype              = detect_role_type(jd)
    overall, secs      = compute_ats_score(model, rtext, jd)
    kw_s, kw_ok, kw_no, kw_tot = keyword_match_score(rtext, jd)
    jdsk               = set(extract_skills(jd, rtype))
    resk               = set(extract_skills(rtext, rtype))
    matched            = sorted(jdsk & resk)
    missing            = sorted(jdsk - resk)
    fmt                = format_feedback(rtext)

    _stop = {"with","that","this","from","have","been","will","your","their","they","were",
             "able","should","must","using","based","work","role","years","strong","level",
             "experience","position","responsibilities","about","also","more","some","other",
             "skills","which","where","what","when","include","including","required","preferred"}
    exp_pat  = r"(?i)(experience|work|built|develop|implement|deploy|deliver|role|position).{0,200}"
    jd_ew    = set(w.strip(".,():;") for ln in _re.findall(exp_pat, jd)
                  for w in ln.lower().split() if len(w.strip(".,():;")) > 4)
    res_ew   = set(w.strip(".,():;") for ln in _re.findall(exp_pat, rtext)
                  for w in ln.lower().split() if len(w.strip(".,():;")) > 4)
    miss_exp = sorted([w for w in (jd_ew-res_ew) if w not in _stop and len(w)>4])[:8]

    tips, qs, ai_q = [], [], ""
    if groq_key:
        raw = get_career_coach(rtext, jd, overall, matched, missing, rtype, groq_key)
        if raw and not raw.startswith("ERROR:"):
            tips, qs, ai_q = parse_coach_output(raw)

st.session_state.update({"results_ready":True,"_has_cv":True,"_has_jd":True})
render_steps(_ph, 3)

quote   = ai_q if ai_q else score_quote(overall)
suggs   = []
for sk in missing[:5]:
    suggs.append(f"Add <strong>{sk}</strong> to your skills section")
for lv, msg in fmt:
    if lv in ("red","amber"): suggs.append(msg)
for t in tips[:3]:
    if t.strip(): suggs.append(t)

rcls = "tag-tech" if rtype == "tech" else "tag-ntech"
rico = "⚙️ Technical Role" if rtype == "tech" else "💼 Non-Technical Role"

st.markdown(f"""<div style="display:flex;align-items:center;gap:10px;margin-bottom:1.6rem;">
    <span class="xm-tag {rcls}">{rico}</span>
    <span style="font-size:0.8rem;color:#7c70a0;font-family:'DM Mono',monospace;">{score_label(overall)}</span>
</div>""", unsafe_allow_html=True)

# ── A. Dual scores ────────────────────────────────────────────────────────────
ca, cb2 = st.columns(2, gap="large")
with ca:
    st.markdown(f"""<div class="xm-score-wrap">
        <div class="xm-score-pill pill-semantic">🧠 Semantic ATS Score</div>
        <div class="xm-score-ring" style="border-color:{col(overall)};color:{col(overall)};">{overall}%</div>
        <div class="xm-score-sub">{score_label(overall)}</div>
        <div style="font-size:0.74rem;color:#7c70a0;margin-top:0.85rem;line-height:1.6;
        max-width:220px;font-style:italic;">
            AI understands meaning — "built ML pipelines" matches "machine learning engineer"
        </div>
    </div>""", unsafe_allow_html=True)

with cb2:
    st.markdown(f"""<div class="xm-score-wrap">
        <div class="xm-score-pill pill-keyword">🔍 Keyword Match Score</div>
        <div class="xm-score-ring" style="border-color:{col(kw_s)};color:{col(kw_s)};">{kw_s}%</div>
        <div class="xm-score-sub">{len(kw_ok)} of {kw_tot} JD keywords found</div>
        <div style="font-size:0.74rem;color:#7c70a0;margin-top:0.85rem;line-height:1.6;
        max-width:220px;font-style:italic;">
            Exact word check — like a basic ATS bot. Low score = may be auto-rejected
        </div>
    </div>""", unsafe_allow_html=True)

st.markdown(f'<div class="xm-quote" style="margin-top:1.3rem;">✦ {quote}</div>',
            unsafe_allow_html=True)

# ── B. Keyword detail ─────────────────────────────────────────────────────────
st.markdown('<div class="xm-card"><div class="xm-card-title">🔍 Keyword Match Detail</div>',
            unsafe_allow_html=True)
kl, kr = st.columns(2, gap="large")
with kl:
    st.markdown("<div style='font-size:0.78rem;font-weight:600;color:#006b4e;margin-bottom:5px;'>✅ Found in your resume</div>", unsafe_allow_html=True)
    tags = "".join(f'<span class="xm-tag tag-kw-ok">{w}</span>' for w in kw_ok[:15])
    st.markdown(tags or "<span style='font-size:0.78rem;color:#7c70a0;'>None found.</span>",
                unsafe_allow_html=True)
with kr:
    st.markdown("<div style='font-size:0.78rem;font-weight:600;color:#92400e;margin-bottom:5px;'>❌ Missing from resume</div>", unsafe_allow_html=True)
    tags = "".join(f'<span class="xm-tag tag-kw-no">{w}</span>' for w in kw_no[:15])
    st.markdown(tags or "<span style='font-size:0.78rem;color:#006b4e;font-weight:600;'>🎉 All matched!</span>",
                unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── C. Section breakdown ──────────────────────────────────────────────────────
descs = {
    "Experience": ["Aligns well with this role","Moderate match — highlight relevant work","Gap detected — emphasise transferable skills"],
    "Skills":     ["Strong skill alignment","Partial match — add missing tools","Low overlap — review JD requirements"],
    "Education":  ["Education fits the role","Partial — highlight relevant courses","Add certifications for this role"],
    "Projects":   ["Projects highly relevant","Some relevance — add role-specific work","Add projects matching JD domain"],
}
def sdesc(n,v): a=descs.get(n,["","",""]); return a[0] if v>=75 else (a[1] if v>=50 else a[2])

ordered = {k: secs[k] for k in ["Experience","Skills","Education","Projects"] if k in secs}
for k,v in secs.items():
    if k not in ordered: ordered[k]=v

st.markdown('<div class="xm-card"><div class="xm-card-title">📊 Section Breakdown</div>',
            unsafe_allow_html=True)
bl, br = st.columns(2, gap="large")
for i,(sec,val) in enumerate(ordered.items()):
    with (bl if i%2==0 else br):
        st.markdown(f"""<div class="xm-bar-wrap">
            <div class="xm-bar-meta"><span>{sec}</span>
            <span style="color:{col(val)};font-weight:800;">{val}%</span></div>
            <div class="xm-bar-track"><div class="xm-bar-fill" style="width:{val}%;background:{grad(val)};"></div></div>
            <div class="xm-bar-desc">{sdesc(sec,val)}</div>
        </div>""", unsafe_allow_html=True)
        if sec == "Experience" and miss_exp:
            kw_html = "".join(f'<span class="tag-exp-kw">{w}</span>' for w in miss_exp)
            st.markdown(f"""<div style="background:rgba(245,158,11,0.07);border:1px solid rgba(245,158,11,0.2);
                border-radius:8px;padding:0.5rem 0.8rem;margin-top:-0.3rem;margin-bottom:0.5rem;">
                <span style="font-size:0.72rem;font-weight:600;color:#92400e;font-family:'DM Mono',monospace;">
                ⚠️ Missing exp keywords:</span>
                <div style="margin-top:4px;line-height:2.2;">{kw_html}</div>
            </div>""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── D. Skill gap ──────────────────────────────────────────────────────────────
st.markdown('<div class="xm-card"><div class="xm-card-title">🎯 Skill Gap Analysis</div>',
            unsafe_allow_html=True)
sl, sr = st.columns(2, gap="large")
with sl:
    st.markdown("<div style='font-size:0.78rem;font-weight:600;color:#006b4e;margin-bottom:5px;'>✅ Skills you have</div>", unsafe_allow_html=True)
    tags = "".join(f'<span class="xm-tag tag-match">{s}</span>' for s in matched)
    st.markdown(tags or "<span style='font-size:0.78rem;color:#7c70a0;'>No curated skills matched.</span>",
                unsafe_allow_html=True)
with sr:
    st.markdown("<div style='font-size:0.78rem;font-weight:600;color:#b91c1c;margin-bottom:5px;'>❌ Skills missing</div>", unsafe_allow_html=True)
    tags = "".join(f'<span class="xm-tag tag-miss">{s}</span>' for s in missing)
    st.markdown(tags or "<span style='font-size:0.78rem;color:#006b4e;font-weight:600;'>🎉 No missing skills!</span>",
                unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── E. Format check ───────────────────────────────────────────────────────────
st.markdown('<div class="xm-card"><div class="xm-card-title">📋 Resume Format Check</div>',
            unsafe_allow_html=True)
fl, fr = st.columns(2, gap="large")
for i,(lv,msg) in enumerate(fmt):
    with (fl if i%2==0 else fr):
        st.markdown(f"""<div class="xm-fmt-row">
            <div class="xm-fmt-dot" style="background:{DOT_COLORS[lv]};"></div>
            <span>{msg}</span></div>""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── F. Suggestions ────────────────────────────────────────────────────────────
if suggs:
    st.markdown('<div class="xm-card"><div class="xm-card-title">💡 Suggestions to Improve Your CV</div>',
                unsafe_allow_html=True)
    for s in suggs:
        if s.strip():
            st.markdown(f'<div class="xm-sugg"><span class="xm-sugg-arrow">→</span><span>{s}</span></div>',
                        unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── G. Interview questions ────────────────────────────────────────────────────
if groq_key and qs:
    st.markdown('<div class="xm-card"><div class="xm-card-title">❓ Interview Questions from Your Resume</div>',
                unsafe_allow_html=True)
    for q in qs[:5]:
        if q.strip():
            st.markdown(f'<div class="xm-question">💬 {q}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

if not groq_key:
    st.markdown("""<div class="xm-api-nudge">
        🔑 <strong>Add your Groq API key in the sidebar</strong>
        to unlock AI coach tips, interview questions, and a smart quote.
    </div>""", unsafe_allow_html=True)

# ── H. Good luck ─────────────────────────────────────────────────────────────
closing = ("You're all set — go get that job!" if overall>=75
           else "Keep refining — every great career starts with a great CV!" if overall>=50
           else "Room to grow — use these tips and come back stronger!")
st.markdown(f"""<div class="xm-luck">
    <div class="xm-luck-title">Good Luck! 🍀</div>
    <div class="xm-luck-sub">{closing}</div>
</div>""", unsafe_allow_html=True)