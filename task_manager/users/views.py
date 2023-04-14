from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.mixins import AuthorizationMixin, UserPermissionMixin
from task_manager.users.forms import UserForm
from task_manager.users.models import User


class UsersListView(ListView):
    template_name = 'users/users_list.html'
    model = User
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    template_name = 'sign.html'
    model = User
    form_class = UserForm
    success_url = reverse_lazy("login")
    success_message = _('UserCreateSuccess')
    extra_context = {
        'title_action': _("Register"),
        'button': _("ButtonSignUp")
    }


class UserUpdateView(SuccessMessageMixin, AuthorizationMixin,
                     UserPermissionMixin, UpdateView):
    template_name = 'form.html'
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users_list')
    success_message = _('UserUpdateSuccess')
    permission_denial_message = _("UserUpdateDenial")
    extra_context = {
        'category': _("Users"),
        'title_action': _("UserUpdate"),
        'button': _("Update")
    }


class UserDeleteView(SuccessMessageMixin, AuthorizationMixin,
                     UserPermissionMixin, DeleteView):
    template_name = 'delete.html'
    model = User
    success_url = reverse_lazy('users_list')
    success_message = _('UserDeleteSuccess')
    permission_denial_message = _("UserDeleteDenial")
    extra_context = {
        'category': _("Users"),
        'title_action': _("UserDelete")
    }

    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=kwargs['pk'])
        if user.author.all() or user.executor.all():
            messages.error(self.request, _("UserOnTaskDeleteDenial"))
            return redirect('/users/')
        else:
            return super().post(self, request, *args, **kwargs)
