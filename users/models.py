from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    image_avatar = models.ImageField(
        null=True, blank=True, upload_to="avatars/", default='avatars/user-default.png')
    company = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.user.username)


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    national_id = models.CharField(
        max_length=20,  null=False)  # Added
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    image_avatar = models.ImageField(
        null=True, blank=True, upload_to="avatars/", default='avatars/user-default.png')
    city = models.CharField(max_length=200, blank=True, null=True)
    bio = models.CharField(max_length=500, blank=True, null=True)
    experience_level = models.CharField(max_length=200, blank=True, null=True)
    programming_languages = models.ManyToManyField(
        'ProgrammingLanguage', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.user.username)


class ProgrammingLanguage(models.Model):
    language = models.CharField(max_length=200, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.language


class ProfileView(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    viewer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.viewer.username)


class Profile(models.Model):
    USER_TYPE_CHOICES = (
        ('employee', 'Employee'),
        ('employer', 'Employer'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return f"{self.user.username} ({self.user_type})"
