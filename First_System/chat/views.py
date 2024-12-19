
# Create your views here.
# auth_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, LoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Registration successful!')
            return redirect('home')  # Redirect to home after registration
    else:
        form = RegistrationForm()

    return render(request, 'chat/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully!')
                return redirect('home')  # Redirect to home after login
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'chat/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login after logout

@login_required
def home(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if user is not authenticated
    usernames = User.objects.values_list('username', flat=True)
    return render(request, 'chat/home.html', {'usernames': usernames})


def room(request, room_name):
    username = request.GET.get('username', 'Anonymous')

    return render(request, 'chat/room.html', {'room_name': room_name, 'username': username})

@login_required
def delete_user(request, username):

    user_to_delete = get_object_or_404(User, username=username)

    if user_to_delete != request.user:
        user_to_delete.delete()
        return redirect('home') 

    return HttpResponseForbidden("You cannot delete your own account.")