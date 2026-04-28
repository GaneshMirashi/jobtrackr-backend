from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from service.gemini_service import analyze_resume
from core.extract_text import extract_text_from_pdf
import json

class ResumeAnalyzerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file = request.FILES.get("file")
        text = request.data.get("text")

        # Extract text from PDF
        if file:
            text = extract_text_from_pdf(file)

            if not text or not text.strip():
                return Response(
                    {"success": False, "message": "Could not extract text from PDF"},
                    status=400
                )

        # Validate input
        if not text or not text.strip():
            return Response(
                {"success": False, "message": "No text provided"},
                status=400
            )

        # AI analysis
        try:
            result = analyze_resume(text)
        except Exception as e:
            return Response(
                {"success": False, "message": str(e)},
                status=500
            )

        # Parse AI response
        try:
            parsed = json.loads(result)
        except json.JSONDecodeError:
            parsed = {"raw": result}

        return Response({
            "success": True,
            "data": parsed
        })