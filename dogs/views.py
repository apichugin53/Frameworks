from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls.base import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from dogs.forms import DogForm
from dogs.models import Dog, Breed
from users.models import Role


class IndexView(TemplateView):
    template_name = 'dogs/index.html'
    extra_context = {
        'title': _('Main page'),
    }


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
            'action_url': reverse_lazy('dogs:dog_update', kwargs={'pk': self.object.id}),
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


class DogDetailsView(DetailView):
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


class BreedsListView(ListView):
    model = Breed
    template_name = 'dogs/breeds_list.html'
    extra_context = {
        'title': _('Breeds'),
    }


class BreedDetailsView(DetailView):
    model = Breed
    template_name = 'dogs/breed_details.html'
    extra_context = {
        'title': _('Breed'),
    }
