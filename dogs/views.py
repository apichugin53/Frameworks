from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Dog, Breed
from .forms import DogForm

def dog_list(request):
    dogs = Dog.objects.select_related('breed', 'owner').all()
    return render(request, 'dogs/dog_list.html', {'dogs': dogs})

@login_required
def add_dog(request):
    if request.method == 'POST':
        form = DogForm(request.POST, request.FILES)
        if form.is_valid():
            dog = form.save(commit=False)
            dog.owner = request.user
            dog.save()
            return redirect('dogs:dog_list')
    else:
        form = DogForm()
    return render(request, 'dogs/add_dog.html', {'form': form})

def dog_detail(request, dog_id):
    dog = get_object_or_404(Dog, id=dog_id)
    return render(request, 'dogs/dog_detail.html', {'dog': dog})
