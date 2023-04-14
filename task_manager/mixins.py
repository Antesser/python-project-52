from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


class AuthorizationMixin(LoginRequiredMixin):
    login_url = 'login/'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(self.request, _("AuthorizationRequired"))
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


class UserPermissionMixin(UserPassesTestMixin):
    def test_func(self):
        is_self_user = self.request.user.pk == self.get_object().pk
        is_superuser = self.request.user.is_superuser
        return is_self_user or is_superuser

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denial_message)
        return redirect('users_list')


class SetAuthorMixin:
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
