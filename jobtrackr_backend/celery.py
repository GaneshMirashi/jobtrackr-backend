import os
from celery.schedules import crontab
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "jobtrackr_backend.settings"
)

# Create a new Celery application instance
app = Celery("jobtrackr_backend")

# Load task modules from all registered Django app configs.
app.config_from_object(
    "django.conf:settings",
    namespace="CELERY"
)

# Define the Celery beat schedule for periodic tasks
app.conf.beat_schedule = {
    "send-interview-reminders-every-morning": {
        "task": "applications.tasks.send_interview_reminders",

        # Every day at 9:00 AM
        "schedule": crontab(hour=9, minute=0),
    },
}

# Autodiscover tasks from all installed apps
app.autodiscover_tasks()