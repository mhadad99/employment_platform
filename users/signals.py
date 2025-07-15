from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import Employer, Employee

from django.core.mail import send_mail
from django.conf import settings

# @receiver(post_save, sender=Profile)


# def createEmployee(sender, instance, created, **kwargs):
#     if created:
#         user = instance
#         employee = Employee.objects.create(
#             user=user,
#             username=user.username,
#             email=user.email,
#             name=user.first_name,
#         )


# def createEmployer(sender, instance, created, **kwargs):
#     if created:
#         user = instance
#         employer = Employer.objects.create(
#             user=user,
#             username=user.username,
#             email=user.email,
#             name=user.first_name,
#         )

        # subject = 'Welcome to DevSearch'
        # message = 'We are glad you are here!'

        # try:
        #     send_mail(
        #         subject,
        #         message,
        #         settings.EMAIL_HOST_USER,
        #         [Employee.email],
        #         fail_silently=False,
        #     )
        # except:
        #     print('Email failed to send...')


def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user

    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass





# post_save.connect(createEmployee, sender=User)
# post_save.connect(createEmployer, sender=User)
post_save.connect(updateUser, sender=Employee)
post_save.connect(updateUser, sender=Employer)
post_delete.connect(deleteUser, sender=Employee)
post_delete.connect(deleteUser, sender=Employer)
