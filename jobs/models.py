from django.db import models

# Create your models here.


class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    programming_languages = models.ManyToManyField(
        'users.ProgrammingLanguage', blank=True)
    employer = models.ForeignKey('users.Employer', on_delete=models.CASCADE)
    employee = models.ForeignKey(
        'users.Employee', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    employee = models.ForeignKey('users.Employee', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), (
        'accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.name} applied for {self.job.title}"
