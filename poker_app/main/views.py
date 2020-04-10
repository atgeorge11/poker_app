from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from .forms import UserForm, LoginForm

def index(request):
    """Home page"""
    return render(request, 'main/index.html')

def register(request):
    """Register a new user"""
    if request.method != 'POST':
        #Display blank registration form
        form = UserForm()
    else:
        #Process completed form
        form = UserForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            #Log the user in and then redirect to home page
            login(request, new_user)
            return redirect('main:index')

    #Display a blank or invalid form
    context = {'form': form}
    return render(request, 'main/register.html', context)

def log_in(request):
    """Login page"""
    if request.method != 'POST':
        #Display an empty form
        form = LoginForm()
        not_found = False
    else:
        #Process completed form
        username = request.POST.dict()['username']

        try:
            user = User.objects.get(username=username)
            login(request, user)
            return render(request, 'main/index.html')

        except ObjectDoesNotExist:
            form = LoginForm()
            not_found = True
            
    return render(request, 'main/login.html', {'form': form, 'not_found': not_found})

def log_out(request):
    """Logout page"""
    logout(request)
    return render(request, 'main/logout.html')
