from django.urls.base import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from dogs.forms import DogForm
from dogs.models import Dog, Breed


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


class DogCreateView(CreateView):
    model = Dog
    form_class = DogForm
    template_name = 'dogs/dog_form.html'
    extra_context = {
        'title': _('Add dog'),
        'action_url': reverse_lazy('dogs:dog_create'),
    }

    def get_success_url(self):
        return reverse('dogs:dog_details', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class DogUpdateView(UpdateView):
    model = Dog
    form_class = DogForm
    template_name = 'dogs/dog_form.html'
    extra_context = {
        'title': _('Edit dog'),
    }

    def get_success_url(self):
        return reverse('dogs:dog_details', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(DogUpdateView, self).get_context_data(**kwargs)
        context['action_url'] = reverse_lazy('dogs:dog_update', kwargs={'pk': self.object.id})
        return context


class DogDetailsView(DetailView):
    model = Dog
    template_name = 'dogs/dog_details.html'
    extra_context = {
        'title': _('Dog'),
    }


class DogDeleteView(DeleteView):
    model = Dog
    success_url = reverse_lazy('dogs:dogs_list')


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
