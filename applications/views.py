from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import JobApplication
from .serializers import JobApplicationSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


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
        serializer.save(user=self.request.user)

    # ✅ Custom endpoint for status update (Kanban)
    @action(detail=True, methods=["patch"])
    def status(self, request, pk=None):
        application = self.get_object()
        new_status = request.data.get("status")

        application.status = new_status
        application.save()

        return Response({
            "success": True,
            "data": JobApplicationSerializer(application).data,
            "message": "Status updated successfully"
        })