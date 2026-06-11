from celery import shared_task

from django.core.mail import send_mail

from django.utils.timezone import now
from datetime import timedelta

from .models import JobApplication


@shared_task
def send_interview_reminders():

    tomorrow = now().date() + timedelta(days=1)

    applications = JobApplication.objects.filter(
        interview_date=tomorrow
    )

    for app in applications:

        if app.user.email:

            send_mail(
                subject="Interview Reminder",

                message=f"""
Hi {app.user.username},

You have an upcoming interview tomorrow.

Company: {app.company_name}
Role: {app.job_title}

Best of luck 🚀
                """,

                from_email="your_email@gmail.com",

                recipient_list=[app.user.email],

                fail_silently=False,
            )

    return "Interview reminders sent"
