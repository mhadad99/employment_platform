from django.dispatch.dispatcher import receiver
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import conf
from django.db.models import Q
from .forms import CustomUserCreationForm, EmployeeRegistrationForm, EmployerRegistrationForm
from .models import Employee, Employer, Profile

# Create your views here.
# home


def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('jobs')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'jobs')

        else:
            messages.error(request, 'Username OR password is incorrect')

    return render(request, 'users/register_login.html')


def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logged out!')
    return redirect('login')


def registerUser(request):
    page = 'register'
    user_type = request.GET.get('user_type')
    if user_type:
        request.session['user_type'] = user_type

    user_form = CustomUserCreationForm()
    employee_form = EmployeeRegistrationForm()
    employer_form = EmployerRegistrationForm()

    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        user_type = request.session.get('user_type')
        if user_type == 'employee':
            employee_form = EmployeeRegistrationForm(request.POST)
            valid = user_form.is_valid() and employee_form.is_valid()
        elif user_type == 'employer':
            employer_form = EmployerRegistrationForm(request.POST)
            valid = user_form.is_valid() and employer_form.is_valid()
        else:
            valid = user_form.is_valid()

        if valid:
            user = user_form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            # Save user_type in Profile
            Profile.objects.create(user=user, user_type=user_type)

            if user_type == 'employee':
                employee = employee_form.save(commit=False)
                employee.user = user
                employee.username = user.username
                employee.email = user.email
                employee.name = user.first_name
                employee.save()
            elif user_type == 'employer':
                employer = employer_form.save(commit=False)
                employer.user = user
                employer.username = user.username
                employer.email = user.email
                employer.name = user.first_name
                employer.save()

            messages.success(request, 'User account was created!')
            login(request, user)
            return redirect('jobs')
        else:
            messages.error(
                request, 'An error has occurred during registration')

    context = {
        'page': page,
        'form': user_form,
        'employee_form': employee_form,
        'employer_form': employer_form,
        'user_type': user_type,
    }
    return render(request, 'users/register_login.html', context)
