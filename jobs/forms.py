from django.db.models.base import Model
from django.forms import ModelForm, widgets
from django import forms
from .models import Job




class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description',
                  'programming_languages',]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'programming_languages': forms.CheckboxSelectMultiple(),
            'employer': forms.Select(attrs={'class': 'form-control'}),
            'employee': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != 'programming_languages':
                field.widget.attrs.update({'class': 'form-control'})
