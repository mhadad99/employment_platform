# urls of users
from django.urls import path
from . import views
from django.urls import path, include


urlpatterns = [
    path('register/', views.registerUser, name='register'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    # path('', views.profiles, name='profiles'),
    # path('user-profile/<str:pk>', views.userProfile, name='user-profile'),
]
