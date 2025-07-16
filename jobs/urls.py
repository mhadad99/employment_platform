# urls.p for jobs
from django.urls import path
from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.jobs, name="jobs"),
    path('job/<str:pk>/', views.job, name="job"),
    path('create-job/', views.createJob, name="create-job"),
    path('delete-job/<str:pk>/', views.deleteJob, name="delete-job"),
    path('update-job/<str:pk>/', views.updateJob, name="update-job"),
    path('apply-job/<str:pk>/', views.applyJob, name='apply-job'),
    path('manage-applications/<str:job_id>/',
         views.manageApplications, name='manage-applications'),
    path('update-application/<str:app_id>/',
         views.updateApplication, name='update-application'),
    path('notifications/', views.notifications, name='notifications'),

]
