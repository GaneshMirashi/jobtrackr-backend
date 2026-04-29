from django.db import models
from django.conf import settings


class JobApplication(models.Model):

    STATUS_CHOICES = [
        ("APPLIED", "Applied"),
        ("SCREENING", "Screening"),
        ("INTERVIEW", "Interview"),
        ("OFFER", "Offer"),
        ("REJECTED", "Rejected"),
        ("WITHDRAWN", "Withdrawn"),
    ]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    position = models.IntegerField(default=0)
    company_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    job_url = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="APPLIED")

    applied_date = models.DateField(null=True, blank=True)
    follow_up_date = models.DateField(blank=True, null=True)

    salary_min = models.IntegerField(blank=True, null=True)
    salary_max = models.IntegerField(blank=True, null=True)

    resume = models.FileField(upload_to="resumes/", null=True, blank=True)

    job_description = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "job_applications"
        ordering = ["-created_at", "position"]

    def __str__(self):
        return f"{self.company_name} - {self.job_title}"