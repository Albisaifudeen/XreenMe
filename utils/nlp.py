import re
import pdfplumber
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import streamlit as st

# ── Skill pools ───────────────────────────────────────────────────────────────
TECH_SKILLS = [
    "python","java","javascript","typescript","c++","c#","r","sql","nosql",
    "machine learning","deep learning","nlp","computer vision","tensorflow",
    "pytorch","keras","scikit-learn","xgboost","transformers","bert","gpt",
    "llm","rag","langchain","huggingface","docker","kubernetes","mlops",
    "mlflow","dvc","airflow","aws","gcp","azure","fastapi","flask","django",
    "rest api","git","ci/cd","linux","spark","hadoop","kafka","pandas",
    "numpy","opencv","yolo","reinforcement learning","generative ai",
    "faiss","chromadb","pinecone","postgresql","mongodb","redis",
    "data engineering","feature engineering","model deployment",
    "a/b testing","statistics","probability","tableau","power bi",
]

NON_TECH_SKILLS = [
    "project management","communication","leadership","agile","scrum",
    "product management","marketing","sales","customer success","finance",
    "accounting","hr","recruiting","operations","strategy","consulting",
    "business development","content writing","seo","social media",
    "data analysis","excel","powerpoint","stakeholder management",
    "presentation","negotiation","budgeting","forecasting","crm",
]

TECH_ROLE_KEYWORDS = [
    "engineer","developer","data scientist","ml engineer","ai engineer",
    "devops","architect","programmer","analyst","researcher","scientist",
    "backend","frontend","fullstack","cloud","security","qa","sre",
]

LEVEL_MAP = {
    "intern": 0, "junior": 1, "associate": 2, "mid": 3,
    "senior": 4, "lead": 5, "principal": 6, "staff": 6,
    "manager": 7, "director": 8, "vp": 9, "head": 8,
}

# ── Common stop words to ignore in keyword matching ───────────────────────────
_KW_STOP = {
    "the","and","for","with","that","this","from","have","been","will",
    "your","their","they","were","able","should","must","using","based",
    "work","role","years","strong","level","about","also","more","some",
    "other","skills","which","where","what","when","include","including",
    "required","preferred","you","are","our","team","join","looking","good",
    "into","over","such","well","both","each","most","than","then","them",
    "these","those","here","there","would","could","make","like","just",
    "very","also","only","but","not","all","any","new","use","used","uses",
    "has","had","its","his","her","who","how","may","get","set","put","run",
}

# ── Model loader ──────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

# ── PDF / Word parser ─────────────────────────────────────────────────────────
def extract_text(uploaded_file):
    """Memory-only extraction — never saved to disk."""
    text = ""
    name = uploaded_file.name.lower()
    try:
        if name.endswith(".pdf"):
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    t = page.extract_text()
                    if t:
                        text += t + "\n"
        elif name.endswith(".docx") or name.endswith(".doc"):
            try:
                import docx
                doc = docx.Document(uploaded_file)
                text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
            except Exception:
                pass
    except Exception:
        pass
    return text.strip()

# ── Role detection ────────────────────────────────────────────────────────────
def detect_role_type(jd_text):
    jd_lower   = jd_text.lower()
    tech_hits  = sum(1 for r in TECH_ROLE_KEYWORDS if r in jd_lower)
    skill_hits = sum(1 for s in TECH_SKILLS if s in jd_lower)
    return "tech" if (tech_hits >= 1 or skill_hits >= 3) else "non-tech"

# ── Skill extractor ───────────────────────────────────────────────────────────
def extract_skills(text, role_type):
    pool       = TECH_SKILLS if role_type == "tech" else NON_TECH_SKILLS
    text_lower = text.lower()
    return list(set(s for s in pool if s in text_lower))

# ── Semantic ATS scorer ───────────────────────────────────────────────────────
def compute_ats_score(model, resume_text, jd_text):
    """
    Semantic scoring using SBERT cosine similarity.
    Understands meaning — 'built ML pipelines' matches 'machine learning engineer'.
    """
    r_emb   = model.encode([resume_text])
    j_emb   = model.encode([jd_text])
    overall = float(cosine_similarity(r_emb, j_emb)[0][0]) * 100

    sections = {
        "Experience": r"(?i)(experience|work|built|develop|implement|deploy|deliver|role|position)",
        "Skills":     r"(?i)(skill|technolog|tool|framework|language|library|proficien)",
        "Education":  r"(?i)(education|degree|university|college|bachelor|master|phd|certif)",
        "Projects":   r"(?i)(project|portfolio|github|built|created|developed|launched|demo)",
    }
    section_scores = {}
    for name, pattern in sections.items():
        res = " ".join(re.findall(pattern + r".{0,200}", resume_text))
        jd  = " ".join(re.findall(pattern + r".{0,200}", jd_text))
        if res and jd:
            section_scores[name] = float(
                cosine_similarity(model.encode([res]), model.encode([jd]))[0][0]
            ) * 100
        else:
            section_scores[name] = overall * 0.88

    return round(overall, 1), {k: round(v, 1) for k, v in section_scores.items()}

# ── Keyword match scorer ──────────────────────────────────────────────────────
def keyword_match_score(resume_text, jd_text):
    """
    Hard keyword matching — counts how many meaningful words from the JD
    appear verbatim in the resume.

    Returns:
        kw_score (float)         — 0–100 percentage
        kw_matched (list[str])   — keywords found in resume
        kw_missing (list[str])   — keywords from JD not in resume
        total_kw   (int)         — total unique JD keywords checked
    """
    def tokenise(text):
        # Extract meaningful words: 4+ chars, alpha only, not in stop list
        words = re.findall(r"[a-zA-Z]{4,}", text.lower())
        return set(w for w in words if w not in _KW_STOP)

    jd_words     = tokenise(jd_text)
    resume_words = tokenise(resume_text)

    if not jd_words:
        return 0.0, [], [], 0

    matched = sorted(jd_words & resume_words)
    missing = sorted(jd_words - resume_words)
    score   = round(len(matched) / len(jd_words) * 100, 1)

    return score, matched, missing, len(jd_words)

# ── Format checker ────────────────────────────────────────────────────────────
def format_feedback(resume_text):
    feedback   = []
    word_count = len(resume_text.split())

    if word_count < 200:
        feedback.append(("red",   f"Too short ({word_count} words) — aim for 400–700 words"))
    elif word_count > 900:
        feedback.append(("amber", f"Might be too long ({word_count} words) — consider trimming"))
    else:
        feedback.append(("green", f"Good length — {word_count} words ✓"))

    bullets = resume_text.count("•") + resume_text.count("·") + resume_text.count("-")
    if bullets < 5:
        feedback.append(("amber", "Add more bullet points for scannability"))
    else:
        feedback.append(("green", f"{bullets} bullet points found — good structure ✓"))

    if re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", resume_text):
        feedback.append(("green", "Email address found ✓"))
    else:
        feedback.append(("red",   "No email detected — add contact info"))

    if re.search(r"(\+?\d[\d\s\-]{7,}\d)", resume_text):
        feedback.append(("green", "Phone number found ✓"))
    else:
        feedback.append(("amber", "Phone number not detected"))

    if "linkedin" in resume_text.lower():
        feedback.append(("green", "LinkedIn profile found ✓"))
    else:
        feedback.append(("amber", "Add your LinkedIn profile URL"))

    found = [s for s in ["experience","education","skills","project","summary","objective"]
             if s in resume_text.lower()]
    if len(found) < 3:
        feedback.append(("red",   f"Only {len(found)} sections found — add Experience, Education, Skills"))
    else:
        feedback.append(("green", f"{len(found)} resume sections detected ✓"))

    return feedback

# ── Job title matcher ─────────────────────────────────────────────────────────
def job_title_match(resume_text, jd_text):
    resume_lower = resume_text.lower()
    jd_lower     = jd_text.lower()

    resume_level = next((v for k, v in LEVEL_MAP.items() if k in resume_lower), 3)
    jd_level     = next((v for k, v in LEVEL_MAP.items() if k in jd_lower), 3)

    diff = abs(resume_level - jd_level)
    if diff == 0:   pct, label = 100, "Exact level match"
    elif diff == 1: pct, label = 75,  "One level off — close fit"
    elif diff == 2: pct, label = 50,  "Two levels difference"
    else:           pct, label = 20,  "Significant level mismatch"

    jd_title = next(
        (w.strip(".,():") for w in jd_text.split()
         if any(r in w.lower() for r in TECH_ROLE_KEYWORDS[:8])),
        "Target Role"
    )
    return pct, label, jd_title

# ── Colour helpers ────────────────────────────────────────────────────────────
def score_color(s):
    if s >= 75: return "#00C896"
    if s >= 50: return "#f59e0b"
    return "#ff4d6d"

def bar_gradient(s):
    if s >= 75: return "linear-gradient(90deg,#00C896,#00a67e)"
    if s >= 50: return "linear-gradient(90deg,#f59e0b,#d97706)"
    return "linear-gradient(90deg,#ff4d6d,#e11d48)"

def score_label(s):
    if s >= 80: return "🟢 Strong Match"
    if s >= 65: return "🟡 Good Match"
    if s >= 50: return "🟠 Moderate Match"
    return "🔴 Needs Work"

DOT_COLORS = {"green": "#00C896", "amber": "#f59e0b", "red": "#ff4d6d"}