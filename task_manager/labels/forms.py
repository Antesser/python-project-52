from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Label


class LabelForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        required=True,
        label=_("Name"),
        error_messages={'unique': _('LabelExistsError')},
        widget=forms.TextInput(attrs={'placeholder': _('Name')}),
    )

    class Meta:
        model = Label
        fields = ('name', )
