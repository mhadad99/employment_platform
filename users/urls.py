# urls of users
from django.urls import path
from . import views
from django.urls import path, include


urlpatterns = [
    path('register/', views.registerUser, name='register'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('', views.employees, name='employees'),
    path('user-profile/<str:pk>', views.userProfile, name='user-profile'),
    path('user-account/', views.userAccount, name='user-account'),
    path('edit-account/', views.editAccount, name='edit-account'),
    path('search-employees/', views.searchEmployees, name='search-employees'),
    path('add-language/', views.add_language, name='add-language'),
    path('delete-language/<str:lang_id>/',
         views.delete_language, name='delete-language'),
]
