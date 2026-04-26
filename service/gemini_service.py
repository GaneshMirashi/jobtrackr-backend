import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")


def analyze_resume(text):
    prompt = f"""
    Analyze this resume and return STRICT JSON:

    {{
      "skills": [],
      "strengths": [],
      "weaknesses": [],
      "suggestions": []
    }}

    Resume:
    {text}
    """

    response = model.generate_content(prompt)

    return response.text