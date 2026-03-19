from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, DetailView, UpdateView

from users.forms import UserEditForm, UserActiveStatusForm, UserRoleForm

User = get_user_model()


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/user_list.html'
    extra_context = {
        'title': _('Users')
    }
    ordering = 'username'
    paginate_by = 8

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)


class SelfMixin:
    def get_object(self, *args, **kwargs):
        if self.pk_url_kwarg in self.kwargs:
            return super().get_object(*args, **kwargs)
        return self.request.user


class ModerationMixin():
    def can_moderate(self):
        actor = self.request.user
        subject = self.object
        if subject == actor or not actor.is_moderator:
            return False
        if subject.is_admin and actor.is_moderator:
            return False
        return True

    def get_context_data(self, **kwargs):
        context = {
            'can_moderate': self.can_moderate(),
            **kwargs,
        }
        return super().get_context_data(**context)


class UserDetailsView(LoginRequiredMixin, ModerationMixin, SelfMixin, DetailView):
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


class UserDogsView(LoginRequiredMixin, ModerationMixin, SelfMixin, DetailView):
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

    def get_context_data(self, **kwargs):
        context = {
            'dogs': self.object.dog_set.all().values('id', 'name', 'photo', 'views'),
            **kwargs,
        }
        return super().get_context_data(**context)


class UserEditView(LoginRequiredMixin, SelfMixin, UpdateView):
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


class UserActiveStatusView(LoginRequiredMixin, ModerationMixin, UpdateView):
    model = User
    form_class = UserActiveStatusForm
    http_method_names = ["post", "options"]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.can_moderate():
            raise PermissionDenied
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('users:user_details', kwargs={'pk': self.object.id})


class UserRoleView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserRoleForm
    http_method_names = ["post", "options"]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.is_admin:
            raise PermissionDenied
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('users:user_details', kwargs={'pk': self.object.id})


class UserCommentsView(LoginRequiredMixin, ModerationMixin, SelfMixin, DetailView):
    model = User
    template_name = 'users/user_comments.html'
    extra_context = {
        'title': _('Profile')
    }

    def get_context_data(self, **kwargs):
        context = {
            'comments': self.object.comment_set.all().select_related('dog'),
            **kwargs,
        }
        return super().get_context_data(**context)

    def get(self, request, *args, **kwargs):
        if self.pk_url_kwarg in self.kwargs:
            pk = self.kwargs[self.pk_url_kwarg]
            if self.request.user.id == pk:
                return redirect('users:profile_comments')
        return super().get(request, *args, **kwargs)
