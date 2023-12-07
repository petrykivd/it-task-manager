from datetime import datetime, timedelta

from django import forms
from django.contrib.auth import get_user_model

from task_manager.models import Task


class TaskCreationForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'task_type', 'deadline', 'assignees', 'priority', 'description']
        widgets = {
            'deadline': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local', 'class': 'form-control'
                },
                format='%Y-%m-%dT%H:%M'
            ),
            'assignees': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(TaskCreationForm, self).__init__(*args, **kwargs)
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_str = tomorrow.strftime('%Y-%m-%dT%H:%M')
        self.fields['deadline'].widget.attrs['min'] = tomorrow_str


class TaskEditForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'task_type', 'deadline', 'assignees', 'priority', 'description']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}, format='%Y-%m-%dT%H:%M'),
            'assignees': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(TaskEditForm, self).__init__(*args, **kwargs)
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_str = tomorrow.strftime('%Y-%m-%dT%H:%M')
        self.fields['deadline'].widget.attrs['min'] = tomorrow_str


class AssignWorkerForm(forms.Form):
    task = forms.ModelChoiceField(queryset=Task.objects.all(), label='Select Task')
    worker = forms.ModelChoiceField(queryset=get_user_model().objects.all(), label='Select Worker')


class WorkerForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = '__all__'


class WorkerSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={'placeholder': '🔍Search by name'})
    )
