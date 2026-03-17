# ⚡ XreenMe — AI Resume Screener

> Semantic resume screening powered by SBERT embeddings + Groq LLaMA3 — beyond keyword matching.

[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Groq](https://img.shields.io/badge/Groq-LLaMA3-orange?style=for-the-badge)](https://console.groq.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

## 🚀 Live Demo

**Try XreenMe Live** — *(add your Streamlit Cloud link after deployment)*

---

## 🧠 What is XreenMe?

XreenMe solves a real problem on both sides of hiring:

- **Job seekers** don't know why their resume gets rejected by ATS bots
- **Recruiters** waste hours manually reading CVs

XreenMe automates and explains both — using real AI (not just keyword counting) to score resumes the way a smart recruiter actually reads them.

---

## ✨ Features

### 👤 Individual Mode — for job seekers

| Feature | Description |
|---|---|
| 🧠 Semantic ATS Score | SBERT embeddings — understands *meaning*, not just keywords |
| 🔍 Keyword Match Score | Exact word check — simulates basic ATS bots |
| 📊 Section Breakdown | Experience, Skills, Education, Projects scored separately |
| ⚠️ Missing Exp Keywords | JD words not found in your experience section |
| 🎯 Skill Gap Analysis | Matched vs missing skills from a curated pool |
| 📋 Format Check | Word count, bullets, email, phone, LinkedIn, sections |
| 💡 Suggestions | Actionable tips to improve your CV |
| ❓ Interview Questions | 5 AI-generated questions from your resume gaps *(needs API)* |
| 🤖 AI Coach Tips | 3 personalised improvement tips *(needs API)* |

### 🏢 Recruiter Mode — for hiring managers

| Feature | Description |
|---|---|
| 📁 Batch Processing | Up to 10 CVs at once |
| 🏆 Candidate Ranking | Ranked by ATS score with 🥇🥈🥉 medals |
| 📊 Dual Scores | Semantic + Keyword scores per candidate |
| 📋 Full Breakdown | Expandable per-candidate analysis |
| 🤖 AI Recommendation | 2-sentence hiring summary per candidate *(needs API)* |
| ⚙️ Role Detection | Auto-detects Tech vs Non-Tech from JD |

---

## 🛠️ Tech Stack

| Layer | Tool | Why |
|---|---|---|
| Semantic Scoring | `sentence-transformers` all-MiniLM-L6-v2 | Fast, runs on CPU, understands meaning |
| Similarity | `scikit-learn` cosine_similarity | Standard vector distance metric |
| Keyword Scoring | Custom `keyword_match_score()` | Simulates basic ATS bots |
| Resume Parsing | `pdfplumber` + `python-docx` | PDF and Word support |
| AI Feedback | `Groq API` → llama3-8b-8192 | Free tier, ultra fast inference |
| UI | `Streamlit` multi-page | Fast to build, easy to deploy free |
| Env Management | `python-dotenv` | Secure API key handling |

---

## 📁 Project Structure

```
XreenMe/
├── app.py                    # Landing page — mode selector + hero
├── requirements.txt          # All dependencies
├── .env                      # Your API key (never commit this!)
├── .env.example              # Template — safe to commit
├── .gitignore
├── README.md
│
├── pages/
│   ├── individual.py         # Individual mode — full CV analysis
│   └── recruiter.py          # Recruiter mode — batch screening
│
├── utils/
│   ├── nlp.py                # Scoring, parsing, skill extraction
│   └── llm.py                # Groq API calls + prompt templates
│
├── components/
│   └── styles.py             # Full CSS design system
│
└── .streamlit/
    └── config.toml           # Streamlit theme config
```

---

## ⚙️ Local Setup

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/xreenme.git
cd xreenme
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

> ⚠️ **Windows users** — install PyTorch CPU version first to avoid DLL errors:
> ```bash
> pip uninstall torch torchvision torchaudio -y
> pip install torch==2.1.0 --index-url https://download.pytorch.org/whl/cpu
> pip install transformers==4.38.0
> ```

### 3. Add your Groq API key
Create a `.env` file:
```
GROQ_API_KEY=your_groq_key_here
```
Get a **free** key at [console.groq.com](https://console.groq.com) — no credit card needed.

### 4. Run
```bash
streamlit run app.py
```
Opens at `http://localhost:8501` ✅

> The app works **without an API key** — AI features (coach tips, interview questions) are unlocked when a key is added.

---

## 📦 Requirements

```
streamlit==1.35.0
pdfplumber==0.11.1
sentence-transformers==3.0.1
scikit-learn==1.5.0
groq==0.9.0
torch==2.1.0
transformers==4.38.0
python-dotenv==1.0.1
python-docx==1.1.2
```

---

## 🌐 Deploy Free on Streamlit Cloud

1. Push this repo to GitHub (make sure `.env` is in `.gitignore`)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select your repo → `app.py` as the main file
5. Add your `GROQ_API_KEY` in the **Secrets** section
6. Click **Deploy** — live URL in ~2 minutes 🚀

---

## 🔐 Privacy

- Resumes processed **in memory only** — never saved to disk
- Session-based — all data cleared when browser closes
- API key stored in `.env` — never exposed in the UI
- `.env` excluded from git via `.gitignore`

---

## 📄 License

MIT — free to use, modify, and deploy.

---

## 👤 Author

Built by **Albi Saif** — AI/CV Engineer  
[LinkedIn](https://linkedin.com/in/YOUR_HANDLE) 