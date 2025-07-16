from django.dispatch import receiver
from jobs.models import Job, Notification
from django.db.models import Q
from django.db.models.signals import post_save, post_delete
from .models import JobApplication, Notification
from users.models import Employee
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def notify_employee_of_matching_jobs(employee):
    # Get programming languages
    langs = employee.programming_languages.values_list('language', flat=True)
    # Get bio keywords (split by space, simple approach)
    bio_keywords = employee.bio.lower().split() if employee.bio else []

    # Find jobs matching programming languages
    jobs_by_lang = Job.objects.filter(
        programming_languages__language__in=langs)
    # Find jobs matching bio keywords in title or description
    jobs_by_bio = Job.objects.none()
    for word in bio_keywords:
        jobs_by_bio |= Job.objects.filter(
            Q(title__icontains=word) | Q(description__icontains=word)
        )

    # Combine and remove duplicates
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

    all_employees = Employee.objects.all()
    bios = [emp.bio for emp in all_employees]

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([job_text] + bios)  

    similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    threshold = 0.2
    matched_employees = [
        emp for emp, score in zip(all_employees, similarities) if score >= threshold
    ]

    employees_by_language = Employee.objects.filter(
        programming_languages__in=job.programming_languages.all()
    ).distinct()

    final_employees = list(set(list(matched_employees) + list(employees_by_language)))

    for employee in final_employees:
        Notification.objects.create(
            recipient=employee,
            message=f"New job '{job.title}' matches your skills or bio!"
        )