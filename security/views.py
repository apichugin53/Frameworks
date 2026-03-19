from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import (LoginView, RedirectURLMixin, PasswordResetView, PasswordResetDoneView,
                                       PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeView,
                                       PasswordChangeDoneView)
from django.shortcuts import redirect, resolve_url
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.utils.translation import gettext_lazy as _

from security.forms import SignUpForm, SignInForm, PwdResetForm

User = get_user_model()


class SignInView(LoginView):
    form_class = SignInForm
    template_name = 'security/signin.html'
    redirect_authenticated_user = True
    extra_context = {
        'title': _('Sign in')
    }


class SignUpView(RedirectURLMixin, CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'security/signup.html'
    extra_context = {
        'title': _('Sign up')
    }
    success_url = reverse_lazy('users:profile')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def get_default_redirect_url(self):
        return resolve_url(self.success_url)

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, self.object)
        return result


class PwdResetView(PasswordResetView):
    email_template_name = "security/password_reset_email.html"
    template_name = 'security/password_reset_form.html'
    success_url = reverse_lazy('auth:password_reset_done')
    form_class = PwdResetForm


class PwdResetDoneView(PasswordResetDoneView):
    template_name = 'security/password_reset_done.html'


class PwdResetConfirmView(PasswordResetConfirmView):
    template_name = 'security/password_reset_confirm.html'
    success_url = reverse_lazy('auth:password_reset_complete')


class PwdResetCompleteView(PasswordResetCompleteView):
    template_name = 'security/password_reset_complete.html'


class PwdChangeView(PasswordChangeView):
    template_name = 'security/password_change_form.html'
    success_url = reverse_lazy('users:profile_edit')
