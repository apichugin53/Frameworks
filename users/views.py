from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import render, redirect

from users.forms import SignInForm, SignUpForm


User = get_user_model()


def sign_in(request):
    if request.method == 'POST':
        form = SignInForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dogs:home')
    else:
        form = SignInForm()

    context = {
        'title': 'Вход',
        'form': form,
    }
    return render(request, 'users/signin.html', context)


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dogs:home')
    else:
        form = SignUpForm()

    context = {
        'title': 'Регистрация',
        'form': form,
    }
    return render(request, 'users/signup.html', context)


def sign_out(request):
    logout(request)
    return redirect('dogs:home')


def profile(request):
    context = {
        'title': 'Профиль пользователя',
        'user': request.user,
    }
    return render(request, 'users/profile.html', context)