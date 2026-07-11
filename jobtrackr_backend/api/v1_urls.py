# jobtrackr_backend/api/v1_urls.py

from django.urls import path, include

urlpatterns = [
    path("auth/", include("users.urls")),
    path("applications/", include("applications.urls")),
    path("resume/", include("resume.urls")),
    path("dashboard/", include("dashboard.urls")),
]