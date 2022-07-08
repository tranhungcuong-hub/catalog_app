from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
def SignIn(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = None
    if request.method == "POST":
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.info(request, 'Invalid Username or Password')
    return render(request, "login.html", {'user': user})


def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        username = request.POST.get('username')
        if form.is_valid():
            form.save()
            messages.success(request, f'Account created for {username}')
        else:
            messages.success(request, form.errors)
            return redirect('register')
        return redirect("login")
    else:
        form = UserForm()
    return render(request, "registration.html", {'form': form})


def homepage(request):
    return render(request, "base.html")


@login_required(login_url='login')
def profile(request):
    return render(request, "user_page.html", {})


def Logout(request):
    logout(request)
    return redirect('home')

