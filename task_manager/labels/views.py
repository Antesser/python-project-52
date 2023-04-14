from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from labels.forms import LabelForm
from labels.models import Label

from task_manager.mixins import AuthorizationMixin


class LabelListView(AuthorizationMixin, ListView):
    template_name = 'labels/labels_list.html'
    model = Label
    context_object_name = 'labels'


class LabelCreateView(SuccessMessageMixin, AuthorizationMixin, CreateView):
    template_name = 'form.html'
    model = Label
    form_class = LabelForm
    success_url = reverse_lazy("labels_list")
    success_message = _('LabelCreateSuccess')
    extra_context = {
        'category': _("Labels"),
        'title_action': _("LabelCreate"),
        'button': _("ButtonCreate")
    }


class LabelUpdateView(SuccessMessageMixin, AuthorizationMixin, UpdateView):
    template_name = 'form.html'
    model = Label
    form_class = LabelForm
    success_url = reverse_lazy('labels_list')
    success_message = _('LabelUpdateSuccess')
    extra_context = {
        'category': _("Labels"),
        'title_action': _("LabelUpdate"),
        'button': _("Update")
    }


class LabelDeleteView(SuccessMessageMixin, AuthorizationMixin, DeleteView):
    template_name = 'delete.html'
    model = Label
    success_url = reverse_lazy('labels_list')
    success_message = _('LabelDeleteSuccess')
    extra_context = {
        'category': _("Labels"),
        'title_action': _("LabelDelete")
    }

    def post(self, request, *args, **kwargs):
        label = Label.objects.get(id=kwargs['pk'])
        if label.task_set.all():
            messages.error(self.request, _("LabelOnTaskDeleteDenial"))
            return redirect('labels_list')
        else:
            return super().post(self, request, *args, **kwargs)
