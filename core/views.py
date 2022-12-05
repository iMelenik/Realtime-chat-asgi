from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import *


# Create your views here.
def index(request):
    return render(request, "core/index.html")


def room(request, room_name):
    return render(request, "core/room.html", {"room_name": room_name})


def register_view(request):
    form = SignUpForm(request.POST or None)
    if request.method == 'POST':
        print(form.errors.as_data())
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    return render(request, 'core/signup.html', context={'form': form})


def login_view(request):
    form = AuthenticationForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            login(request, form.get_user())
            return redirect('index')
    return render(request, 'core/login.html', context={'form': form})
