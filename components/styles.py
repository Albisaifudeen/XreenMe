MAIN_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=DM+Mono:ital,wght@0,400;0,500;1,400&display=swap');

:root {
    --bg:       #f5f4fb;
    --card:     #ffffff;
    --card2:    #faf9ff;
    --border:   #e8e4f3;
    --border2:  #cec6e8;
    --ink:      #09090f;
    --ink2:     #3d3557;
    --ink3:     #7c70a0;
    --green:    #00b884;
    --green2:   #009e70;
    --gfaint:   rgba(0,184,132,0.08);
    --amber:    #f59e0b;
    --red:      #ef4444;
    --blue:     #3b82f6;
    --purple:   #7c3aed;
    --r:        10px;
    --rlg:      16px;
    --rxl:      22px;
    --sh:       0 1px 4px rgba(80,60,140,0.07), 0 4px 16px rgba(80,60,140,0.06);
    --sh2:      0 2px 8px rgba(80,60,140,0.08), 0 12px 40px rgba(80,60,140,0.10);
}

html, body {
    font-family: 'Outfit', sans-serif !important;
    background: #f5f4fb !important;
    color: #09090f !important;
}

.stApp,
.stApp > div, .stApp > div > div,
.main, .main > div, section.main,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > div,
[data-testid="stAppViewBlockContainer"],
[data-testid="stAppViewBlockContainer"] > div,
[data-testid="block-container"],
[data-testid="stVerticalBlock"],
[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stMain"], [data-testid="stMainBlockContainer"],
div[class*="appview"], div[class*="appview-container"] {
    background: #f5f4fb !important;
}

[data-testid="stSidebar"], [data-testid="stSidebarContent"] {
    background: #ffffff !important;
    border-right: 1px solid #e8e4f3 !important;
}

#MainMenu, footer, header, [data-testid="stToolbar"] { visibility: hidden !important; }

.block-container {
    padding-top: 2.5rem !important;
    padding-bottom: 5rem !important;
    max-width: 1160px !important;
}

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #f5f4fb; }
::-webkit-scrollbar-thumb { background: #cec6e8; border-radius: 99px; }

/* ── Buttons ── */
.stButton > button {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    background: #09090f !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: var(--r) !important;
    padding: 0.68rem 1.6rem !important;
    width: 100% !important;
    transition: all 0.18s ease !important;
    box-shadow: 0 2px 8px rgba(9,9,15,0.18) !important;
    letter-spacing: 0.1px !important;
}
.stButton > button:hover {
    background: #1c1c2e !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 18px rgba(9,9,15,0.25) !important;
}
.back-btn .stButton > button {
    background: transparent !important;
    color: var(--ink3) !important;
    border: 1px solid var(--border2) !important;
    font-size: 0.78rem !important;
    padding: 0.34rem 0.9rem !important;
    box-shadow: none !important;
    width: auto !important;
    font-weight: 500 !important;
    transform: none !important;
}
.back-btn .stButton > button:hover {
    color: var(--ink) !important;
    border-color: var(--ink) !important;
    transform: none !important;
    box-shadow: none !important;
}

/* ── Inputs ── */
textarea, .stTextArea textarea {
    background: #ffffff !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--r) !important;
    color: var(--ink) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.87rem !important;
    box-shadow: var(--sh) !important;
}
textarea:focus, .stTextArea textarea:focus {
    border-color: var(--ink) !important;
    box-shadow: 0 0 0 3px rgba(9,9,15,0.06) !important;
}
[data-testid="stFileUploader"] { background: #ffffff !important; border-radius: var(--r) !important; }
[data-testid="stFileUploaderDropzone"] {
    background: #ffffff !important;
    border: 1.5px dashed var(--border2) !important;
    border-radius: var(--r) !important;
}
[data-testid="stFileUploaderDropzone"]:hover { border-color: var(--ink) !important; }
div[data-testid="stExpander"] {
    background: #ffffff !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r) !important;
    box-shadow: var(--sh) !important;
}
div[data-testid="stExpander"] summary { color: var(--ink2) !important; font-size: 0.84rem !important; }

/* ── Hero ── */
.xm-hero {
    background: linear-gradient(140deg, #0d0b1e 0%, #1a0a36 55%, #0f0d28 100%);
    border-radius: var(--rxl);
    padding: 3.2rem 3.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.xm-hero::before {
    content:''; position:absolute; top:-100px; right:-100px;
    width:400px; height:400px; border-radius:50%;
    background:radial-gradient(circle,rgba(0,184,132,0.1) 0%,transparent 65%);
}
.xm-hero::after {
    content:''; position:absolute; bottom:-60px; left:8%;
    width:260px; height:260px; border-radius:50%;
    background:radial-gradient(circle,rgba(124,58,237,0.12) 0%,transparent 65%);
}
.xm-eyebrow {
    font-family:'DM Mono',monospace; font-size:0.6rem; font-weight:500;
    letter-spacing:4px; text-transform:uppercase; color:var(--green); margin-bottom:0.6rem;
}
.xm-hero-title {
    font-family:'Outfit',sans-serif; font-weight:900; font-size:3.8rem;
    color:#ffffff; letter-spacing:-2px; line-height:1; margin-bottom:0.7rem;
}
.xm-hero-title span { color:var(--green); }
.xm-hero-sub { font-size:0.95rem; color:rgba(255,255,255,0.55); line-height:1.65; max-width:500px; margin-bottom:1.4rem; }
.xm-hero-quote {
    display:inline-flex; align-items:center; gap:10px;
    background:rgba(0,184,132,0.1); border:1px solid rgba(0,184,132,0.22);
    border-radius:99px; padding:0.55rem 1.2rem;
    font-size:0.82rem; color:var(--green); font-style:italic; font-family:'DM Mono',monospace;
}

/* ── Mode cards ── */
.xm-card-mode {
    background:#ffffff; border:1.5px solid var(--border);
    border-radius:var(--rxl); padding:2rem; height:100%;
    transition:all 0.22s ease; cursor:pointer; position:relative; overflow:hidden;
    box-shadow:var(--sh);
}
.xm-card-mode::after {
    content:''; position:absolute; top:0; left:0; right:0; height:3px;
    background:linear-gradient(90deg,var(--green),var(--purple)); opacity:0; transition:opacity 0.22s;
}
.xm-card-mode:hover { border-color:var(--border2); transform:translateY(-3px); box-shadow:var(--sh2); }
.xm-card-mode:hover::after { opacity:1; }
.xm-mode-icon { font-size:2rem; margin-bottom:0.9rem; }
.xm-mode-title { font-family:'Outfit',sans-serif; font-size:1.45rem; font-weight:800; color:var(--ink); letter-spacing:-0.4px; margin-bottom:0.25rem; }
.xm-mode-sub { font-size:0.82rem; color:var(--ink3); margin-bottom:1.3rem; }
.xm-mode-feat { display:flex; align-items:flex-start; gap:9px; padding:0.45rem 0; font-size:0.83rem; color:var(--ink2); border-bottom:1px solid var(--border); line-height:1.5; }
.xm-mode-feat:last-of-type { border-bottom:none; }
.xm-feat-dot { color:var(--green); font-size:0.5rem; flex-shrink:0; margin-top:5px; }

/* ── Result cards ── */
.xm-card {
    background:#ffffff; border:1.5px solid var(--border);
    border-radius:var(--rlg); padding:1.5rem; margin-bottom:1.1rem; box-shadow:var(--sh);
}
.xm-card-title {
    font-family:'DM Mono',monospace; font-size:0.56rem; font-weight:500;
    letter-spacing:4px; text-transform:uppercase; color:var(--ink3);
    margin-bottom:1.1rem; padding-bottom:0.75rem; border-bottom:1.5px solid var(--border);
}

/* ── Score rings ── */
.xm-score-wrap {
    background:#ffffff; border:1.5px solid var(--border); border-radius:var(--rlg);
    padding:1.8rem 1.4rem; display:flex; flex-direction:column;
    align-items:center; text-align:center; box-shadow:var(--sh); position:relative; overflow:hidden;
}
.xm-score-ring {
    width:158px; height:158px; border-radius:50%; border:8px solid;
    display:flex; align-items:center; justify-content:center;
    font-family:'Outfit',sans-serif; font-size:1.85rem; font-weight:900;
    letter-spacing:-1px; margin:0.5rem auto 0.8rem auto;
}
.xm-score-sub { font-family:'DM Mono',monospace; font-size:0.57rem; letter-spacing:3px; text-transform:uppercase; color:var(--ink3); }
.xm-score-pill {
    display:inline-flex; align-items:center; gap:6px; font-family:'DM Mono',monospace;
    font-size:0.58rem; letter-spacing:2px; text-transform:uppercase;
    padding:4px 12px; border-radius:99px; margin-bottom:0.7rem; font-weight:500;
}
.pill-semantic { background:var(--gfaint); color:var(--green2); border:1px solid rgba(0,184,132,0.25); }
.pill-keyword  { background:rgba(59,130,246,0.07); color:#2563eb; border:1px solid rgba(59,130,246,0.2); }

/* ── Progress bars ── */
.xm-bar-wrap { margin-bottom:1.1rem; }
.xm-bar-meta { display:flex; justify-content:space-between; font-size:0.85rem; font-weight:600; margin-bottom:6px; color:var(--ink); }
.xm-bar-track { background:#f0eeff; border-radius:99px; height:7px; overflow:hidden; }
.xm-bar-fill { height:100%; border-radius:99px; }
.xm-bar-desc { font-size:0.72rem; color:var(--ink3); margin-top:4px; font-style:italic; }

/* ── Tags ── */
.xm-tag { display:inline-block; padding:3px 11px; border-radius:99px; font-size:0.71rem; font-weight:500; margin:2px; }
.tag-match { background:rgba(0,184,132,0.09); color:#006b4e; border:1px solid rgba(0,184,132,0.25); }
.tag-miss  { background:rgba(239,68,68,0.07);  color:#b91c1c; border:1px solid rgba(239,68,68,0.18); }
.tag-kw-ok { background:rgba(59,130,246,0.08); color:#1d4ed8; border:1px solid rgba(59,130,246,0.2); }
.tag-kw-no { background:rgba(245,158,11,0.09); color:#92400e; border:1px solid rgba(245,158,11,0.2); }
.tag-tech  { background:rgba(59,130,246,0.08); color:#1d4ed8; border:1px solid rgba(59,130,246,0.2);  font-size:0.67rem; padding:3px 9px; border-radius:99px; display:inline-block; }
.tag-ntech { background:rgba(124,58,237,0.08); color:#6d28d9; border:1px solid rgba(124,58,237,0.2); font-size:0.67rem; padding:3px 9px; border-radius:99px; display:inline-block; }
.tag-exp-kw{ background:rgba(245,158,11,0.09); color:#92400e; border:1px solid rgba(245,158,11,0.2); border-radius:99px; padding:2px 8px; font-size:0.69rem; margin:2px; display:inline-block; }

/* ── Format rows ── */
.xm-fmt-row { display:flex; align-items:center; gap:10px; padding:0.55rem 0; border-bottom:1px solid var(--border); font-size:0.82rem; color:var(--ink2); }
.xm-fmt-row:last-child { border-bottom:none; }
.xm-fmt-dot { width:7px; height:7px; border-radius:50%; flex-shrink:0; }

/* ── Quote ── */
.xm-quote {
    border-left:3px solid var(--green); padding:0.85rem 1.2rem;
    background:var(--gfaint); border-radius:0 var(--r) var(--r) 0;
    font-style:italic; font-size:0.88rem; color:var(--green2);
    margin-bottom:1.5rem; font-family:'DM Mono',monospace;
}

/* ── Suggestions ── */
.xm-sugg { display:flex; gap:11px; align-items:flex-start; padding:0.65rem 0; border-bottom:1px solid var(--border); font-size:0.84rem; color:var(--ink2); line-height:1.6; }
.xm-sugg:last-child { border-bottom:none; }
.xm-sugg-arrow { color:var(--green); flex-shrink:0; font-size:0.95rem; margin-top:2px; }

/* ── Interview questions ── */
.xm-question { background:var(--gfaint); border-left:3px solid var(--green); border-radius:0 var(--r) var(--r) 0; padding:0.8rem 1rem; margin-bottom:0.55rem; font-size:0.84rem; color:var(--ink2); line-height:1.6; }

/* ── Rank cards ── */
.xm-rank-card {
    background:#ffffff; border:1.5px solid var(--border); border-radius:var(--rlg);
    padding:1.1rem 1.3rem; margin-bottom:0.8rem;
    display:flex; align-items:flex-start; gap:1rem;
    box-shadow:var(--sh); transition:all 0.18s;
}
.xm-rank-card:hover { border-color:var(--border2); box-shadow:var(--sh2); transform:translateY(-1px); }
.xm-rank-medal { font-size:1.7rem; min-width:36px; text-align:center; flex-shrink:0; padding-top:2px; }
.xm-rank-name { font-family:'Outfit',sans-serif; font-weight:700; font-size:0.92rem; color:var(--ink); margin-bottom:2px; }
.xm-rank-detail { font-size:0.72rem; color:var(--ink3); font-family:'DM Mono',monospace; margin-bottom:6px; }
.xm-rank-scores { display:flex; gap:16px; align-items:center; flex-wrap:wrap; margin-bottom:6px; }
.xm-rank-score-item { display:flex; align-items:center; gap:5px; }
.xm-rank-score-label { font-size:0.68rem; color:var(--ink3); font-family:'DM Mono',monospace; }
.xm-rank-score-val { font-family:'Outfit',sans-serif; font-weight:800; font-size:0.92rem; }

/* ── Step bar ── */
.xm-steps { display:flex; align-items:center; margin-bottom:2rem; }
.xm-step-item { display:flex; align-items:center; gap:8px; }
.xm-step-dot { width:28px; height:28px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:0.7rem; font-weight:700; font-family:'DM Mono',monospace; flex-shrink:0; transition:all 0.25s; }
.xm-step-dot.done   { background:rgba(0,184,132,0.12); color:var(--green2); border:1.5px solid rgba(0,184,132,0.3); }
.xm-step-dot.active { background:var(--ink); color:#fff; }
.xm-step-dot.pending{ background:#f0eeff; color:var(--ink3); border:1.5px solid var(--border); }
.xm-step-label { font-size:0.78rem; font-weight:600; font-family:'Outfit',sans-serif; }
.xm-step-label.done   { color:var(--green2); }
.xm-step-label.active { color:var(--ink); }
.xm-step-label.pending{ color:var(--ink3); }
.xm-step-line { flex:1; height:1.5px; background:var(--border); margin:0 10px; }

/* ── Misc ── */
.xm-divider { border:none; border-top:1.5px solid var(--border); margin:2rem 0; }
.xm-file-pill {
    background:rgba(0,184,132,0.07); border:1px solid rgba(0,184,132,0.2);
    border-radius:var(--r); padding:6px 13px; margin-top:5px;
    display:flex; justify-content:space-between; align-items:center;
}
.xm-api-nudge { background:var(--card2); border:1.5px solid var(--border); border-radius:var(--r); padding:1rem 1.3rem; font-size:0.83rem; color:var(--ink3); line-height:1.8; margin-bottom:1.1rem; }
.xm-luck {
    background:linear-gradient(135deg, #09090f 0%, #1a0a36 100%);
    border-radius:var(--rlg); padding:2rem 2.5rem; text-align:center; margin-top:0.5rem; position:relative; overflow:hidden;
}
.xm-luck::before { content:''; position:absolute; top:-35px; right:-35px; width:150px; height:150px; border-radius:50%; background:rgba(0,184,132,0.08); }
.xm-luck-title { font-family:'Outfit',sans-serif; font-size:1.7rem; font-weight:900; color:#fff; letter-spacing:-0.5px; margin-bottom:0.35rem; }
.xm-luck-sub { font-size:0.88rem; color:rgba(255,255,255,0.55); font-weight:500; }
.xm-ai-note { background:#fafafa; border:1.5px solid var(--border); border-radius:var(--r); padding:0.8rem 1rem; font-size:0.81rem; color:var(--ink2); line-height:1.6; margin-bottom:0.8rem; }
</style>
"""

DOT_COLORS = {"green": "#00b884", "amber": "#f59e0b", "red": "#ef4444"}