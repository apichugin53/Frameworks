from django.http.response import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls.base import reverse

from dogs.forms import DogForm
from dogs.models import Dog, Breed


def index(request):
    context = {
        'title': 'Главная страница',
    }
    return render(request, 'dogs/index.html', context)

def dogs_list(request):
    context = {
        'title': 'Список собак',
        'dogs': Dog.objects.all()
    }
    return render(request, 'dogs/dogs_list.html', context)


def dog_details(request, pk_id):
    context = {
        'title': 'Описание собаки',
        'dog': get_object_or_404(Dog, pk=pk_id),
    }
    return render(request, 'dogs/dog_details.html', context)


def dog_create(request):
    if request.method == 'POST':
        form = DogForm(request.POST, request.FILES)
        if form.is_valid():
            dog = form.save()
            return redirect('dogs:dog_details', dog.id)
    context = {
        'form': DogForm(),
        'action_url': reverse('dogs:dog_create'),
        'action_text': 'Добавить'
    }
    return render(request, 'dogs/dog_form.html', context)


def dog_update(request, pk_id):
    dog = get_object_or_404(Dog, pk=pk_id)
    if request.method == 'POST':
        form = DogForm(request.POST, request.FILES, instance=dog)
        if form.is_valid():
            form.save()
            return redirect('dogs:dog_details', dog.id)
    context = {
        'form': DogForm(instance=dog),
        'action_url': reverse('dogs:dog_update', args=[pk_id]),
        'action_text': 'Обновить'
    }
    return render(request, 'dogs/dog_form.html', context)


def dog_delete(request, pk_id):
    if request.method == 'POST':
        dog = get_object_or_404(Dog, pk=pk_id)
        dog.delete()
        return redirect('dogs:dogs_list')
    raise Http404


def breeds_list(request):
    context = {
        'title': 'Список пород',
        'breeds': Breed.objects.all()
    }
    return render(request, 'dogs/breeds_list.html', context)


def breed_details(request, pk_id):
    context = {
        'title': 'Описание породы',
        'breed': get_object_or_404(Breed, pk=pk_id),
    }
    return render(request, 'dogs/breed_details.html', context)
