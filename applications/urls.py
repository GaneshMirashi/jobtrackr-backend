from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import JobApplicationViewSet, analytics_view, calendar_events, export_applications_csv

router = DefaultRouter()
router.register(r'', JobApplicationViewSet, basename='applications')

urlpatterns = [
    *router.urls,
    path("calendar-events/", calendar_events),
    path("export/csv/",export_applications_csv),
    path("analytics/", analytics_view),
]
