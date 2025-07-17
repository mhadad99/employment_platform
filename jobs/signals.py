from django.dispatch import receiver
from jobs.models import Job, Notification
from django.db.models import Q
from django.db.models.signals import post_save, post_delete

from jobs.utils import match_emplyees
from .models import JobApplication, Notification
from users.models import Employee



def notify_employee_of_matching_jobs(employee):
    langs = employee.programming_languages.values_list('language', flat=True)
    bio_keywords = employee.bio.lower().split() if employee.bio else []

    jobs_by_lang = Job.objects.filter(
        programming_languages__language__in=langs)
    jobs_by_bio = Job.objects.none()
    for word in bio_keywords:
        jobs_by_bio |= Job.objects.filter(
            Q(title__icontains=word) | Q(description__icontains=word)
        )

    matching_jobs = (jobs_by_lang | jobs_by_bio).distinct()

    if matching_jobs.exists():
        job_titles = ', '.join(
            [job.title for job in matching_jobs[:5]])  # limit to 5
        message = f"Jobs matching your skills: {job_titles}"
        Notification.objects.create(
            recipient=employee,
            message=message
        )


@receiver(post_save, sender=Employee)
def employee_post_save(sender, instance, created, **kwargs):
    notify_employee_of_matching_jobs(instance)


@receiver(post_save, sender=JobApplication)
def notify_employer_on_application(sender, instance, created, **kwargs):
    if created:
        employer = instance.job.employer
        message = f"{instance.employee.name} applied for your job '{instance.job.title}'."
        # You may want to create a Notification model for Employer as well,
        # and send a notification to the employer
        Notification.objects.create(
            recipient=employer,
            message=message
        )
        print(message)


@receiver(post_save, sender=Job)
def notify_employees_on_new_job(sender, instance, created, **kwargs):
    if not created:
        return

    job = instance
    job_text = job.title + ' ' + job.description


    final_employees = match_emplyees(job_text)
    if not final_employees:
        return

    for employee in final_employees:
        Notification.objects.create(
            recipient=employee,
            message=f"New job '{job.title}' matches your skills or bio!"
        )