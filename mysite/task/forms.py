from django import forms 
from .models import Task


class TaskForms(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['tittle', 'describe', 'important']