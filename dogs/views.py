from django.shortcuts import render


def index(request):
    context = {
        'title': 'Главная страница',
    }
    return render(request, 'dogs/index.html', context)

def dogs_list(request):
    context = {
        'title': 'Список собак'
    }
    return render(request, 'dogs/dogs_list.html', context)


def dog_details(request, id):
    context = {
        'title': f'Описание собаки',
        'id': id,
    }
    return render(request, 'dogs/dog_details.html', context)


def breeds_list(request):
    context = {
        'title': f'Список пород'
    }
    return render(request, 'dogs/breeds_list.html', context)


def breed_details(request, id):
    context = {
        'title': f'Описание породы',
        'id': id,
    }
    return render(request, 'dogs/breed_details.html', context)
