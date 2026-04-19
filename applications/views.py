from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import JobApplication
from .serializers import JobApplicationSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Count
from collections import defaultdict


class JobApplicationViewSet(ModelViewSet):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = ["status"]
    search_fields = ["company_name", "job_title"]
    ordering_fields = ["applied_date", "created_at"]

    def get_queryset(self):
        queryset = JobApplication.objects.filter(user=self.request.user)

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

        serializer.save(user=user, position=last_position)

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

        grouped = defaultdict(list)

        for app in queryset:
            grouped[app.status].append(JobApplicationSerializer(app).data)

        return Response({
            "success": True,
            "data": grouped,
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

        application.status = new_status
        application.position = new_position
        application.save()

        return Response({
            "success": True,
            "data": JobApplicationSerializer(application).data,
            "message": "Application moved successfully"
        })
    

    # ✅ Custom endpoint for bulk reordering within the same status
    @action(detail=False, methods=["patch"])
    def reorder(self, request):
        data = request.data  # list of objects

        for item in data:
            try:
                app = JobApplication.objects.get(id=item["id"], user=request.user)
                app.position = item["position"]
                app.save()
            except JobApplication.DoesNotExist:
                continue

        return Response({
            "success": True,
            "data": {},
            "message": "Reordered successfully"
        })