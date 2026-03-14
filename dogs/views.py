from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls.base import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from dogs.forms import DogForm, CommentForm
from dogs.models import Dog, Breed, Comment
from users.models import Role


class DogsListView(ListView):
    model = Dog
    template_name = 'dogs/dogs_list.html'
    extra_context = {
        'title': _('Dogs'),
    }


class DogCreateView(LoginRequiredMixin, CreateView):
    model = Dog
    form_class = DogForm
    template_name = 'dogs/dog_form.html'
    extra_context = {
        'title': _('Add dog'),
        'action_url': reverse_lazy('dogs:dog_create'),
    }

    def get(self, request, *args, **kwargs):
        self.object = Dog(owner=self.request.user)
        return self.render_to_response(self.get_context_data())

    def get_success_url(self):
        return reverse('dogs:dog_details', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        actor = self.request.user
        if actor.role == Role.USER:
            form.instance.owner = self.request.user
        return super().form_valid(form)


class DogUpdateView(LoginRequiredMixin, UpdateView):
    model = Dog
    form_class = DogForm
    template_name = 'dogs/dog_form.html'
    extra_context = {
        'title': _('Edit dog'),
    }

    def get_success_url(self):
        return reverse('dogs:dog_details', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = {
            'action_url': reverse('dogs:dog_update', kwargs={'pk': self.object.id}),
            **kwargs,
        }
        return super().get_context_data(**context)

    def get_object(self, queryset=None):
        dog = super().get_object(queryset)
        actor = self.request.user
        if dog.owner == actor or actor.is_staff:
            return dog
        raise PermissionDenied

    def form_valid(self, form):
        actor = self.request.user
        if actor.role == Role.USER:
            form.instance.owner = self.request.user
        return super().form_valid(form)


class DogDetailsView(LoginRequiredMixin, DetailView):
    model = Dog
    template_name = 'dogs/dog_details.html'
    extra_context = {
        'title': _('Dog'),
    }

    def get(self, request, *args, **kwargs):
        result = super().get(request, *args, **kwargs)
        self.object.update_views(self.request.user)
        return result

    def get_context_data(self, **kwargs):
        dog = self.object
        actor = self.request.user
        context = {
            'can_edit': actor.is_authenticated and (dog.owner == actor or actor.is_staff),
            'comments': dog.comment_set.all(),
            **kwargs,
        }
        return super().get_context_data(**context)


class DogDeleteView(LoginRequiredMixin, DeleteView):
    model = Dog
    success_url = reverse_lazy('dogs:dogs_list')

    def get_object(self, queryset=None):
        dog = super().get_object(queryset)
        actor = self.request.user
        if dog.owner == actor or actor.is_staff:
            return dog
        raise PermissionDenied


class BreedsListView(LoginRequiredMixin, ListView):
    model = Breed
    template_name = 'dogs/breeds_list.html'
    extra_context = {
        'title': _('Breeds'),
    }


class BreedDetailsView(LoginRequiredMixin, DetailView):
    model = Breed
    template_name = 'dogs/breed_details.html'
    extra_context = {
        'title': _('Breed'),
    }


class DogCommentAddView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'dogs/comment_form.html'
    extra_context = {
        'title': _('Add comment'),
    }

    def get_context_data(self, **kwargs):
        context = {
            'user': self.request.user,
            'dog': Dog.objects.get(pk=self.kwargs['pk']),
            **kwargs,
        }
        return super().get_context_data(**context)

    def get_success_url(self):
        return reverse('dogs:dog_details', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        context = self.get_context_data()
        instance = form.instance
        instance.user = context['user']
        instance.dog = context['dog']
        return super().form_valid(form)


class DogCommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'dogs/comment_form.html'
    extra_context = {
        'title': _('Edit comment'),
    }

    def get_success_url(self):
        return reverse('dogs:dog_details', kwargs={'pk': self.object.dog.id})
