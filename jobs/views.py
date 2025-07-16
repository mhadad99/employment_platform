from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Job, JobApplication, Notification
from .forms import JobForm
from users.models import ProgrammingLanguage, Employee

# Create your views here.


def jobs(request):
    jobs = Job.objects.all()
    context = {'jobs': jobs}
    return render(request, 'jobs/jobs.html', context)


def job(request, pk):
    jobObj = Job.objects.get(id=pk)

    return render(request, 'jobs/single-job.html', {'job': jobObj})


@login_required(login_url="login")
def createJob(request):
    # Check if the user is an employer
    try:
        employer = request.user.employer
    except AttributeError:
        messages.error(request, "Only employers can post jobs.")
        return redirect('jobs')

    form = JobForm()

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = employer
            job.save()
            form.save_m2m()  # Save many-to-many relationships for programming_languages

            # Handle new languages
            new_languages_raw = request.POST.get('newLanguages', '')
            if new_languages_raw:
                new_languages = new_languages_raw.replace(',', ' ').split()
                for lang_name in new_languages:
                    lang_obj, created = ProgrammingLanguage.objects.get_or_create(
                        language=lang_name)
                    job.programming_languages.add(lang_obj)

            return redirect('jobs')

    context = {'form': form}
    return render(request, "jobs/job-form.html", context)


@login_required(login_url="login")
def updateJob(request, pk):
    # Ensure only the employer can update their own job
    try:
        employer = request.user.employer
    except AttributeError:
        messages.error(request, "Only employers can update jobs.")
        return redirect('jobs')

    job = employer.job_set.get(id=pk)
    form = JobForm(instance=job)

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = employer
            job.save()
            form.save_m2m()  # Save many-to-many relationships for programming_languages

            # Handle new languages
            new_languages_raw = request.POST.get('newLanguages', '')
            if new_languages_raw:
                new_languages = new_languages_raw.replace(',', ' ').split()
                for lang_name in new_languages:
                    lang_obj, created = ProgrammingLanguage.objects.get_or_create(
                        language=lang_name)
                    job.programming_languages.add(lang_obj)

            return redirect('jobs')

    context = {'form': form, 'job': job}
    return render(request, "jobs/job-form.html", context)


@login_required(login_url="login")
def deleteJob(request, pk):
    employer = request.user.employer
    job = employer.job_set.get(id=pk)
    if request.method == 'POST':
        job.delete()
        return redirect('jobs')
    context = {'object': job}
    return render(request, 'delete_template.html', context)


@login_required(login_url="login")
def applyJob(request, pk):
    job = Job.objects.get(id=pk)
    employee = request.user.employee
    # Prevent duplicate applications
    if not JobApplication.objects.filter(job=job, employee=employee).exists():
        JobApplication.objects.create(job=job, employee=employee)
        messages.success(request, "Application submitted!")
    else:
        messages.info(request, "You have already applied for this job.")
    return redirect('job', pk=pk)


@login_required(login_url="login")
def manageApplications(request, job_id):
    employer = request.user.employer
    job = employer.job_set.get(id=job_id)
    applications = JobApplication.objects.filter(job=job)
    context = {'job': job, 'applications': applications}
    return render(request, 'jobs/manage_applications.html', context)


@login_required(login_url="login")
def updateApplication(request, app_id):
    application = JobApplication.objects.get(id=app_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'accept':
            application.status = 'accepted'
            message = f"Your application for '{application.job.title}' has been accepted!"
        elif action == 'reject':
            application.status = 'rejected'
            message = f"Your application for '{application.job.title}' has been rejected."
        application.save()

        # Send notification to employee
        Notification.objects.create(
            recipient=application.employee,
            message=message
        )

    return redirect('manage-applications', job_id=application.job.id)


@login_required(login_url="login")
def notifications(request):
    employee = request.user.employee
    notes = Notification.objects.filter(recipient=employee).order_by('-created_at')
    # Mark all as read
    notes.update(is_read=True)
    return render(request, 'jobs/notifications.html', {'notifications': notes})


