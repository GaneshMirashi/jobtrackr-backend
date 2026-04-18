from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)

            return Response({
                "success": True,
                "data": {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
                "message": "User registered successfully."
            })
        
        return Response({
            "success": False,
            "data": serializer.errors,
            "message": "Validation failed."
        }, status=status.HTTP_400_BAD_REQUEST)
    



class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password
        )

        if user is not None:
            refresh = RefreshToken.for_user(user)

            return Response({
                "success": True,
                "data": {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
                "message": "Login successful."
            })
        return Response({
            "success": False,
            "data": {},
            "message": "Invalid credentials."
        }, status=status.HTTP_401_UNAUTHORIZED)



class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        return Response({
            "success": True,
            "data": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
            },
            "message": "Profile retrieved successfully."
        })



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({
                "success": True,
                "data": {},
                "message": "Logout successful"
            })
        except Exception:
            return Response({
                "success": False,
                "data": {},
                "message": "Invalid token"
            }, status=400)