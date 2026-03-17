from groq import Groq
import re

def get_career_coach(resume_text, jd_text, score, matched, missing, role_type, groq_key):
    """
    Returns career coach tips + interview questions for individual mode.
    Uses structured prompt so output is easy to parse.
    """
    try:
        client = Groq(api_key=groq_key)
        prompt = f"""You are a supportive career coach and senior technical recruiter.

Role Type: {role_type.upper()}
ATS Match Score: {score}%
Skills the candidate HAS that match JD: {', '.join(matched[:10]) if matched else 'None detected'}
Skills MISSING from candidate resume: {', '.join(missing[:8]) if missing else 'None detected'}

Job Description (first 600 chars):
{jd_text[:600]}

Resume (first 600 chars):
{resume_text[:600]}

Analyze the gap between this CV and the Job Description.

Respond in EXACTLY this format (no extra text):

TIPS:
1. [Specific actionable tip to improve resume for this JD]
2. [Specific actionable tip about a missing skill or experience]
3. [Specific tip about presentation, framing, or keywords]

INTERVIEW_QUESTIONS:
1. [Question based on a strength in resume]
2. [Question probing a gap or missing skill]
3. [Situational question based on role]
4. [Technical or behavioral question]
5. [Career progression or motivation question]

QUOTE:
[One short inspiring witty quote about career journeys — make it relevant to their score of {score}%]"""

        resp = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600,
            temperature=0.7,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"ERROR:{str(e)}"


def get_recruiter_summary(resume_text, jd_text, score, matched, missing, role_type, groq_key):
    """
    Short 2-sentence recruiter summary for batch mode.
    """
    try:
        client = Groq(api_key=groq_key)
        prompt = f"""You are a recruiter. In exactly 2 sentences:
1. Would you shortlist this candidate for a {role_type} role? Why?
2. What is their single strongest selling point?

ATS Score: {score}%
Matched skills: {', '.join(matched[:6]) if matched else 'None'}
Missing skills: {', '.join(missing[:4]) if missing else 'None'}
Resume (first 350 chars): {resume_text[:350]}"""

        resp = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=180,
            temperature=0.6,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return ""


def parse_coach_output(raw):
    """Parse structured LLM output into tips, questions, quote."""
    tips, questions, quote = [], [], ""

    try:
        if "TIPS:" in raw:
            tip_block = raw.split("TIPS:")[1].split("INTERVIEW_QUESTIONS:")[0]
            tips = [re.sub(r"^\d+\.\s*", "", line).strip()
                    for line in tip_block.splitlines()
                    if re.match(r"^\d+\.", line.strip())]

        if "INTERVIEW_QUESTIONS:" in raw:
            q_block = raw.split("INTERVIEW_QUESTIONS:")[1].split("QUOTE:")[0]
            questions = [re.sub(r"^\d+\.\s*", "", line).strip()
                         for line in q_block.splitlines()
                         if re.match(r"^\d+\.", line.strip())]

        if "QUOTE:" in raw:
            quote = raw.split("QUOTE:")[1].strip().strip('"').strip("'")

    except Exception:
        pass

    return tips, questions, quote


def score_quote(score):
    """Fallback quotes if LLM doesn't provide one."""
    if score >= 80:
        return "Ready for the interview? Because your resume certainly is."
    elif score >= 60:
        return "You're close — great resumes aren't written, they're rewritten."
    else:
        return "The best resumes aren't written; they are rewritten. Let's tweak the details."


LANDING_QUOTE = "Your resume is a map, not the territory. Let's make sure the path is clear."