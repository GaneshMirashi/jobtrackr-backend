import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")


def analyze_resume(text):
    prompt = f"""
    Analyze the following resume and return:

    1. Key Skills (bullet points)
    2. Strengths
    3. Weaknesses
    4. Suggestions for improvement

    Resume:
    {text}
    """

    response = model.generate_content(prompt)

    return response.text