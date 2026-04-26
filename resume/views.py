from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..service.gemini_service import analyze_resume
from ..core.extract_text import extract_text_from_pdf
import json

class ResumeAnalyzerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file = request.FILES.get("file")
        text = request.data.get("text")

        if file:
            text = extract_text_from_pdf(file)

        if not text:
            return Response({"success": False}, status=400)

        result = analyze_resume(text)

        try:
            parsed = json.loads(result)
        except:
            parsed = {"raw": result}  # fallback

        return Response({
            "success": True,
            "data": parsed
        })