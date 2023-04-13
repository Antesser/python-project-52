from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.mixins import AuthorizationMixin

from .forms import StatusForm
from .models import Status


class StatusListView(AuthorizationMixin, ListView):
    template_name = 'statuses/statuses_list.html'
    model = Status
    context_object_name = 'statuses'


class StatusCreateView(SuccessMessageMixin, AuthorizationMixin, CreateView):
    template_name = 'form.html'
    model = Status
    form_class = StatusForm
    success_url = reverse_lazy("statuses_list")
    success_message = _('StatusCreateSuccess')
    extra_context = {
        'category': _("Statuses"),
        'title_action': _("StatusCreate"),
        'button': _("ButtonCreate")
    }


class StatusUpdateView(SuccessMessageMixin, AuthorizationMixin, UpdateView):
    template_name = 'form.html'
    model = Status
    form_class = StatusForm
    success_url = reverse_lazy('statuses_list')
    success_message = _('StatusUpdateSuccess')
    extra_context = {
        'category': _("Statuses"),
        'title_action': _("StatusUpdate"),
        'button': _("Update")
    }


class StatusDeleteView(SuccessMessageMixin, AuthorizationMixin, DeleteView):
    template_name = 'delete.html'
    model = Status
    success_url = reverse_lazy('statuses_list')
    success_message = _('StatusDeleteSuccess')
    extra_context = {
        'category': _("Statuses"),
        'title_action': _("StatusDelete")
    }

    def post(self, request, *args, **kwargs):
        status = Status.objects.get(id=kwargs['pk'])
        if status.task_set.all():
            messages.error(self.request, _("StatusOnTaskDeleteDenial"))
            return redirect('/statuses/')
        else:
            return super().post(self, request, *args, **kwargs)
