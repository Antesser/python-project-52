from django import forms
from django.utils.translation import gettext_lazy as _

from task_manager.labels.forms import Label
from task_manager.statuses.forms import Status
from task_manager.users.forms import User

from .models import Task


class TaskForm(forms.ModelForm):
    name = forms.CharField(
        max_length=150,
        required=True,
        label=_("Name"),
        error_messages={'unique': _('TaskExistsError')},
        widget=forms.TextInput(attrs={'placeholder': _('Name')}),
    )
    description = forms.CharField(
        label=_("Description"),
        widget=forms.Textarea(attrs={
            'placeholder': _('Description'),
            'cols': 40,
            'rows': 10}),
    )
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        label=_('Status'),
        required=True,
        empty_label=_('SelectStatus')
    )
    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label=_('Executor'),
        required=False,
        empty_label=_('SelectExecutor')
    )

    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        label=_('Labels'),
        required=False
    )

    class Meta:
        model = Task
        fields = ('name', 'description', 'status', 'executor', 'labels')
