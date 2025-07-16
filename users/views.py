from django.dispatch.dispatcher import receiver
from .models import Employee, Employer, Profile, ProgrammingLanguage, ProfileView
from .forms import CustomUserCreationForm, EmployeeRegistrationForm, EmployerRegistrationForm, EmployeeForm
from django.db.models import Q
from django.urls import conf
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from jobs.models import Notification
from datetime import timedelta



# Create your views here.


@login_required(login_url='login')
@require_POST
def add_language(request):
    employee = Employee.objects.get(user=request.user)
    lang_name = request.POST.get('language', '').strip()
    if lang_name:
        lang_obj, created = ProgrammingLanguage.objects.get_or_create(
            language=lang_name)
        employee.programming_languages.add(lang_obj)
    return redirect('user-account')



@login_required(login_url='login')
@require_POST
def delete_language(request, lang_id):
    employee = Employee.objects.get(user=request.user)
    try:
        lang_obj = ProgrammingLanguage.objects.get(id=lang_id)
        employee.programming_languages.remove(lang_obj)
    except ProgrammingLanguage.DoesNotExist:
        pass
    return redirect('user-account')





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
            return redirect(request.GET['next'] if 'next' in request.GET else 'employees')

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


def employees(request):
    employees = Employee.objects.all()
    context = {'employees': employees}
    return render(request, 'users/employees.html', context)


# def userProfile(request, pk):
#     employee = Employee.objects.get(id=pk)
#     context = {'employee': employee}
#     return render(request, 'users/user-profile.html', context)

def userProfile(request, pk):
    employee = get_object_or_404(Employee, id=pk)
    current_user = request.user

    # Only log profile view if the viewer is authenticated and not the employee themselves
    if current_user.is_authenticated and current_user != employee.user:
        try:
            # Prevent duplicate views within 24 hours
            recent_view = ProfileView.objects.filter(
                employee=employee,
                viewer=current_user,
                timestamp__gte=timezone.now() - timedelta(hours=24)
            ).exists()

            if not recent_view:
                ProfileView.objects.create(employee=employee, viewer=current_user)

                message = f"{current_user.first_name} viewed your profile."
                Notification.objects.create(
                    recipient=employee,
                    message=message
                )

        except Exception as e:
            pass

    context = {'employee': employee}
    return render(request, 'users/user-profile.html', context)


# @login_required(login_url='login')
# def userAccount(request):
#     # check user type and redirect to appropriate profile page
#     if request.user.profile.user_type == 'employee':
#         employee = Employee.objects.get(user=request.user)
#         applications = employee.jobapplication_set.all()
#         context = {'employee': employee,
#                    'user_type': request.user.profile.user_type, 'applications': applications}
#     elif request.user.profile.user_type == 'employer':
#         employer = Employer.objects.get(user=request.user)
#         context = {'employer': employer,
#                    'user_type': request.user.profile.user_type}
#     else:
#         messages.error(request, 'Invalid user type')
#         return redirect('login')
#     return render(request, 'users/user-account.html', context)


@login_required(login_url='login')
def userAccount(request):
    if request.user.profile.user_type == 'employee':
        employee = Employee.objects.get(user=request.user)
        applications = employee.jobapplication_set.all()
        
        # Get total profile views
        total_views = ProfileView.objects.filter(employee=employee).count()

        context = {
            'employee': employee,
            'user_type': request.user.profile.user_type,
            'applications': applications,
            'total_profile_views': total_views
        }
    elif request.user.profile.user_type == 'employer':
        employer = Employer.objects.get(user=request.user)
        context = {
            'employer': employer,
            'user_type': request.user.profile.user_type
        }
    else:
        messages.error(request, 'Invalid user type')
        return redirect('login')

    return render(request, 'users/user-account.html', context)


@login_required(login_url='login')
def editAccount(request):
    employee = request.user.employee
    form = EmployeeForm(instance=employee)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()

            return redirect('user-account')

    context = {'form': form}
    return render(request, 'users/employee_form.html', context)


def searchEmployees(request):
    employees = Employee.objects.all()
    query = request.GET.get('q', '')
    language = request.GET.get('language', '')
    city = request.GET.get('city', '')
    experience = request.GET.get('experience', '')

    if query:
        employees = employees.filter(bio__icontains=query)
    if language:
        employees = employees.filter(
            programming_languages__language__iexact=language)
    if city:
        employees = employees.filter(city__iexact=city)
    if experience:
        employees = employees.filter(experience_level__iexact=experience)

    employees = employees.distinct()
    languages = ProgrammingLanguage.objects.all()
    context = {
        'employees': employees,
        'languages': languages,
        'query': query,
        'language': language,
        'city': city,
        'experience': experience,
    }
    return render(request, 'users/employees.html', context)
