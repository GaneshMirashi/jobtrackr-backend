from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import JobApplicationViewSet, NotificationViewSet,CalendarEventsView, analytics_view, calendar_events, export_applications_csv

router = DefaultRouter()
router.register(r'', JobApplicationViewSet, basename='applications')
router.register(r'notifications', NotificationViewSet,basename='notifications')

urlpatterns = [
    *router.urls,
    path("calendar-events/", calendar_events),
    path("export/csv/",export_applications_csv),
    path("analytics/", analytics_view),
    path("calendar/events/",CalendarEventsView.as_view()),
]
