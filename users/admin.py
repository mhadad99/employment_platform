from django.contrib import admin
from .models import Employer, Employee, Profile, ProfileView, ProgrammingLanguage

# Register your models here.


admin.site.register(Employer)
admin.site.register(Employee)
admin.site.register(Profile)
admin.site.register(ProfileView)
admin.site.register(ProgrammingLanguage)
