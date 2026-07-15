from email.mime import application
from urllib import request
from django.db.models.functions import TruncMonth
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ApplicationActivity, JobApplication, Notification
from .serializers import JobApplicationSerializer, NotificationSerializer,ApplicationActivitySerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Count
from collections import defaultdict
from django.db.models import Q
from django.utils.timezone import now
from datetime import timedelta
from rest_framework.decorators import api_view, permission_classes
import csv
from django.http import HttpResponse



class JobApplicationViewSet(ModelViewSet):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = ["status"]
    search_fields = ["company_name", "job_title"]
    ordering_fields = ["applied_date", "created_at"]

    def get_queryset(self):
        queryset = JobApplication.objects.filter(user=self.request.user)
        search = self.request.query_params.get("search")
        status = self.request.query_params.get("status")

        if search:
            queryset = queryset.filter(
                Q(company_name__icontains=search) |
                Q(job_title__icontains=search)
            )

        if status:
            queryset = queryset.filter(status=status)

        # 📅 Date range filtering
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")

        if start_date and end_date:
            queryset = queryset.filter(applied_date__range=[start_date, end_date])

        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        status_value = serializer.validated_data.get("status", "APPLIED")

        last_position = JobApplication.objects.filter(
            user=user,
            status=status_value
        ).count()

        # SAVE APPLICATION
        application = serializer.save(
            user=user,
            position=last_position
        )

        # CREATE ACTIVITY
        ApplicationActivity.objects.create(
            application=application,
            action="Application Created",
            # description=f"Application created for {application.company_name}"
        )

        # CREATE NOTIFICATION
        Notification.objects.create(
            user=user,

            title="Application Added",

            message=f"You applied to {application.company_name}"
        )

    # ✅ Log activity on update
    def perform_update(self, serializer):
        application = serializer.save()

        ApplicationActivity.objects.create(
            application=application,
            action="Application updated"
        )

    # ✅ Custom endpoint for status update (Kanban)
    @action(detail=True, methods=["patch"])
    def status(self, request, pk=None):
        application = self.get_object()
        new_status = request.data.get("status")

        if new_status not in dict(JobApplication.STATUS_CHOICES):
            return Response({
                "success": False,
                "message": "Invalid status"
            }, status=400)

        application.status = new_status
        application.save()

        ApplicationActivity.objects.create(
            application=application,
            action=f"Status changed to {new_status}"
        )

        return Response({
            "success": True,
            "data": JobApplicationSerializer(application).data,
            "message": "Status updated successfully"
        })
    

    @action(detail=False, methods=["get"])
    def stats(self, request):
        user = request.user
        queryset = JobApplication.objects.filter(user=user)

        total = queryset.count()

        status_data = queryset.values("status").annotate(count=Count("status"))

        # Convert to dictionary
        status_counts = {item["status"]: item["count"] for item in status_data}
        recent = queryset.order_by("-created_at")[:5]

        return Response({
            "success": True,
            "data": {
                "total": total,
                "status_counts": status_counts,
                "recent_applications": JobApplicationSerializer(recent, many=True).data
            },
            "message": "Stats fetched successfully"
        })
    

    # ✅ Custom endpoint for fetching Kanban data
    @action(detail=False, methods=["get"])
    def kanban(self, request):
        queryset = self.get_queryset().order_by("position")

        statuses = dict(JobApplication.STATUS_CHOICES).keys()

        data = {status: [] for status in statuses}

        for app in queryset:
            data[app.status].append(JobApplicationSerializer(app).data)

        return Response({
            "success": True,
            "data": data,
            "message": "Kanban data fetched"
        })
    

    # ✅ Custom endpoint for moving application to a different status/position (Drag & Drop)
    @action(detail=True, methods=["patch"])
    def move(self, request, pk=None):
        application = self.get_object()

        new_status = request.data.get("status")
        new_position = request.data.get("position")

        if new_status not in dict(JobApplication.STATUS_CHOICES):
            return Response({
                "success": False,
                "message": "Invalid status"
            }, status=400)

        if new_position is None:
            return Response({
                "success": False,
                "message": "Position is required"
            }, status=400)

        # Get all apps in target column
        apps = JobApplication.objects.filter(
            user=request.user,
            status=new_status
        ).order_by("position")

        # Insert into correct position
        apps = list(apps)
        apps.insert(new_position, application)

        # Reassign positions cleanly
        for index, app in enumerate(apps):
            app.status = new_status
            app.position = index
            app.save()

        return Response({
            "success": True,
            "data": JobApplicationSerializer(application).data,
            "message": "Application moved successfully"
        })

    # ✅ Custom endpoint for bulk reordering within the same status
    @action(detail=False, methods=["patch"])
    def reorder(self, request):
        data = request.data

        apps_map = {
            app.id: app
            for app in JobApplication.objects.filter(user=request.user)
        }

        for item in data:
            app = apps_map.get(item["id"])
            if app:
                app.position = item["position"]

        JobApplication.objects.bulk_update(apps_map.values(), ["position"])

        return Response({
            "success": True,
            "message": "Reordered successfully"
        })


    @action(detail=False, methods=["get"])
    def reminders(self, request):
        today = now().date()
        upcoming = today + timedelta(days=7)

        queryset = JobApplication.objects.filter(
            user=request.user,
            follow_up_date__range=[today, upcoming]
        )

        return Response({
            "success": True,
            "data": JobApplicationSerializer(queryset, many=True).data
        })
    

    @action(detail=True, methods=["get"])
    def activities(self, request, pk=None):
        application = self.get_object()

        activities = application.activities.all()

        serializer = ApplicationActivitySerializer(
            activities,
            many=True
        )

        return Response({
            "success": True,
            "data": serializer.data
        })
    

    @action(detail=False, methods=["get"])
    def analytics(self, request):
        queryset = JobApplication.objects.filter(
            user=request.user
        )

        monthly = (
            queryset
            .annotate(month=TruncMonth("applied_date"))
            .values("month")
            .annotate(count=Count("id"))
            .order_by("month")
        )

        monthly_data = [
            {
                "month": item["month"].strftime("%b"),
                "count": item["count"],
            }
            for item in monthly
        ]

        total = queryset.count()

        offers = queryset.filter(status="OFFER").count()

        success_rate = (
            round((offers / total) * 100, 2)
            if total > 0
            else 0
        )

        upcoming_interviews = queryset.filter(
            interview_date__isnull=False
        ).order_by("interview_date")[:5]

        return Response({
            "success": True,
            "data": {
                "monthly_applications": monthly_data,
                "success_rate": success_rate,
                "upcoming_interviews":
                    JobApplicationSerializer(
                        upcoming_interviews,
                        many=True
                    ).data,
            }
        })







@api_view(["GET"])
@permission_classes([IsAuthenticated])
def calendar_events(request):

    applications = JobApplication.objects.filter(
        user=request.user
    )

    events = []

    for app in applications:

        # Interview Date
        if app.interview_date:
            events.append({
                "title": f"{app.company_name} Interview",
                "date": str(app.interview_date),
                "color": "#2563eb",
            })

        # Follow Up
        if app.follow_up_date:
            events.append({
                "title": f"{app.company_name} Follow Up",
                "date": str(app.follow_up_date),
                "color": "#f59e0b",
            })

        # Applied Date
        if app.applied_date:
            events.append({
                "title": f"Applied to {app.company_name}",
                "date": str(app.applied_date),
                "color": "#10b981",
            })

    return Response(events)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def export_applications_csv(request):

    response = HttpResponse(content_type="text/csv")

    response["Content-Disposition"] = (
        'attachment; filename="applications.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([
        "Company",
        "Job Title",
        "Status",
        "Applied Date",
        "Interview Date",
    ])

    applications = JobApplication.objects.filter(
        user=request.user
    )

    for app in applications:
        writer.writerow([
            app.company_name,
            app.job_title,
            app.status,
            app.applied_date,
            app.interview_date,
        ])

    return response




@api_view(["GET"])
def analytics_view(request):

    queryset = JobApplication.objects.filter(
        user=request.user
    )

    monthly = (
        queryset
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total=Count("id"))
        .order_by("month")
    )

    total = queryset.count()

    interviews = queryset.filter(
        status="INTERVIEW"
    ).count()

    offers = queryset.filter(
        status="OFFER"
    ).count()

    rejected = queryset.filter(
        status="REJECTED"
    ).count()

    success_rate = (
        (offers / total) * 100
        if total > 0 else 0
    )

    return Response({
        "monthly": monthly,
        "total": total,
        "interviews": interviews,
        "offers": offers,
        "rejected": rejected,
        "success_rate": round(success_rate, 2),
    })



class NotificationViewSet(ModelViewSet):

    serializer_class = NotificationSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Notification.objects.filter(
            user=self.request.user
        ).order_by("-created_at")
    






from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from applications.models import JobApplication


class CalendarEventsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        applications = JobApplication.objects.filter(
            user=request.user
        )

        events = []

        for app in applications:

            if app.interview_date:
                events.append({
                    "title": f"{app.company_name} - Interview",
                    "start": app.interview_date,
                    "color": "#2563eb",
                })

            if app.follow_up_date:
                events.append({
                    "title": f"{app.company_name} - Follow Up",
                    "start": app.follow_up_date,
                    "color": "#f59e0b",
                })

        return Response(events)