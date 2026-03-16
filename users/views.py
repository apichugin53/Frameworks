from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, DetailView, UpdateView

from users.forms import UserEditForm, UserStatusForm

User = get_user_model()


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/user_list.html'
    extra_context = {
        'title': _('Users')
    }
    paginate_by = 8

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)


class UserDetailsView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/user_details.html'
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


class UserDogsView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/user_dogs.html'
    extra_context = {
        'title': _('Profile')
    }

    def get(self, request, *args, **kwargs):
        if self.pk_url_kwarg in self.kwargs:
            pk = self.kwargs[self.pk_url_kwarg]
            if self.request.user.id == pk:
                return redirect('users:profile_dogs')
        return super().get(request, *args, **kwargs)

    def get_object(self, *args, **kwargs):
        if self.pk_url_kwarg in self.kwargs:
            return super().get_object(*args, **kwargs)
        return self.request.user

    def get_context_data(self, **kwargs):
        context = {
            'dogs': self.get_object().dog_set.all(),
            **kwargs,
        }
        return super().get_context_data(**context)


class UserEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'users/user_edit.html'
    extra_context = {
        'title': _('Profile')
    }

    def get(self, request, *args, **kwargs):
        if self.pk_url_kwarg in self.kwargs:
            pk = self.kwargs[self.pk_url_kwarg]
            if self.request.user.id == pk:
                return redirect('users:profile_edit')
            else:
                raise PermissionDenied
        return super().get(request, *args, **kwargs)

    def get_object(self, *args, **kwargs):
        if self.pk_url_kwarg in self.kwargs:
            return super().get_object(*args, **kwargs)
        return self.request.user


class UserStatusView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserStatusForm
    http_method_names = ["post", "options"]

    def get_success_url(self):
        return reverse('users:user_details', kwargs={'pk': self.object.id})


class UserCommentsView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/user_comments.html'
    extra_context = {
        'title': _('Profile')
    }

    def get_context_data(self, **kwargs):
        context = {
            'comments': self.get_object().comment_set.all(),
            **kwargs,
        }
        return super().get_context_data(**context)
