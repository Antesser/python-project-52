from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'sign.html'
    next_page = reverse_lazy('index')
    success_message = _('UserLogIn')
    extra_context = {
        'title_action': _("Enter"),
        'button': _("ButtonSignIn")
    }


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _('UserLogOut'))
        return super().dispatch(request, *args, **kwargs)


class PageNotFoundView(TemplateView):
    template_name = '404.html'
