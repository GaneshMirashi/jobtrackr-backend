import google.generativeai as genai
import os
import json
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("models/gemini-flash-latest")

def analyze_resume(text, job_role):
    prompt = f"""
You are an expert ATS Resume Analyzer.

Compare the resume with the target job role.

Job Role:
{job_role}

Resume:
{text}

Return ONLY valid JSON.

{{
  "ats_score": 86,
  "match_percentage": 84,
  "skills": [],
  "missing_skills": [],
  "strengths": [],
  "weaknesses": [],
  "suggestions": [],
  "summary": "",
  "keyword_match": {{
      "matched": [],
      "missing": []
  }}
}}

Rules:

ATS Score must be between 0-100.

Match Percentage must be between 0-100.

Do not return markdown.

Always return JSON.
"""

    response = model.generate_content(prompt)
    raw = response.text.strip()

    # 🔥 Clean common issues (important)
    raw = raw.replace("```json", "").replace("```", "").strip()

    # 🔥 Validate JSON before returning
    try:
        parsed = json.loads(raw)
        return json.dumps(parsed)  # always return clean JSON string
    except json.JSONDecodeError:
        return json.dumps({
            "skills": [],
            "strengths": [],
            "weaknesses": [],
            "suggestions": [],
            "error": "Invalid AI response",
            "raw": raw
        })