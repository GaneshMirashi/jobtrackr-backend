import google.generativeai as genai
import os
import json
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods:
        print(m.name)

model = genai.GenerativeModel("models/gemini-flash-latest")

def analyze_resume(text, job_role):
    prompt = f"""
You are an advanced ATS Resume Analyzer AI.

Compare the candidate resume with the target job role.

Target Job Role:
{job_role}

Resume:
{text}

Return ONLY valid JSON.

JSON format:

{{
  "match_score": 85,
  "matching_skills": ["Python", "Django"],
  "missing_skills": ["Docker", "AWS"],
  "strengths": ["Good backend experience"],
  "weaknesses": ["No cloud deployment projects"],
  "suggestions": ["Add Docker deployment project"],
  "summary": "Candidate is a strong fit for backend roles."
}}

Rules:
- Return only JSON
- No markdown
- No explanations
- Keep points short
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