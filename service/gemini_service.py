import google.generativeai as genai
import os
import json
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods:
        print(m.name)

model = genai.GenerativeModel("models/gemini-flash-latest")
# model = genai.GenerativeModel("models/gemini-pro-latest")

def analyze_resume(text):
    prompt = f"""
You are a resume analyzer.

Return ONLY valid JSON. Do not add explanations, text, or markdown.

JSON format:
{{
  "skills": ["..."],
  "strengths": ["..."],
  "weaknesses": ["..."],
  "suggestions": ["..."]
}}

Rules:
- Always return all keys
- Use short bullet points
- If something is missing, return empty array []
- Do NOT wrap in ``` or markdown

Resume:
{text}
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