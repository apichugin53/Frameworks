from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, RedirectURLMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, resolve_url
from django.urls.base import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from users.forms import SignInForm, SignUpForm, UserUpdateForm

User = get_user_model()


class SignInView(LoginView):
    form_class = SignInForm
    template_name = 'users/signin.html'
    redirect_authenticated_user = True
    extra_context = {
        'title': _('Log in')
    }


class SignUpView(RedirectURLMixin, CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'users/signup.html'
    extra_context = {
        'title': _('Register')
    }
    success_url = reverse_lazy('dogs:home')

    def get_default_redirect_url(self):
        if self.next_page:
            return resolve_url(self.next_page)
        return resolve_url('users:profile')

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, self.object)
        return result

class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    extra_context = {
        'title': _('Profile')
    }

    def get(self, request, *args, **kwargs):
        if self.pk_url_kwarg in self.kwargs:
            pk = self.kwargs[self.pk_url_kwarg]
            if self.request.user.id == pk:
                return redirect('users:profile')
        return super().get(request, *args, **kwargs)

    def get_object(self, *args, **kwargs):
        if self.pk_url_kwarg in self.kwargs:
            return super().get_object(*args, **kwargs)
        return self.request.user


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm

    def get(self, request, *args, **kwargs):
        raise PermissionDenied

    def get_success_url(self):
        return reverse_lazy('users:user_details', kwargs={'pk': self.object.id})
