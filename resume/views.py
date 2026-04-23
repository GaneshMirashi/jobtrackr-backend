from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..service.gemini_service import analyze_resume


class ResumeAnalyzerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        text = request.data.get("text")

        if not text:
            return Response({
                "success": False,
                "message": "No text provided"
            }, status=400)

        result = analyze_resume(text)

        return Response({
            "success": True,
            "data": result
        })