from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResumeAnalyzerView

router = DefaultRouter()


urlpatterns = [
    path("resume-analyze/", ResumeAnalyzerView.as_view()),
]

