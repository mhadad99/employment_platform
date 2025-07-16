from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Employee, Employer


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {'first_name': 'Name'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update(
            {'placeholder': 'Name'})
        self.fields['username'].widget.attrs.update(
            {'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update(
            {'placeholder': 'Email'})
        self.fields['password1'].widget.attrs.update(
            {'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'placeholder': 'Confirm Password'})


class EmployeeRegistrationForm(forms.ModelForm):
    EXPERIENCE_CHOICES = [
        ('Junior', 'Junior'),
        ('Mid', 'Mid'),
        ('Senior', 'Senior'),
    ]
    experience_level = forms.ChoiceField(
        choices=EXPERIENCE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    bio = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control'}), required=True)

    class Meta:
        model = Employee
        fields = ['national_id', 'experience_level', 'city', 'bio']
        widgets = {
            'national_id': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_national_id(self):
        national_id = self.cleaned_data.get('national_id')
        if not national_id.isdigit():
            raise forms.ValidationError(
                "National ID must contain only digits.")
        if len(national_id) != 14:
            raise forms.ValidationError(
                "National ID must be exactly 14 digits.")
        return national_id


class EmployerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ['company']
        widgets = {
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}),
        }


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'email', 'username',
                  'city', 'bio', 'image_avatar', 'experience_level', 'national_id',]

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
