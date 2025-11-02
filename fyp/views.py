from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import UserProfile

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        interests = request.POST.getlist('interests')
        if password != password2:
            messages.error(request, "Passwords do not match")
        elif len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            user = User.objects.create_user(username=username, password=password)
            UserProfile.objects.create(user=user, preferences=interests)
            messages.success(request, "Account created! You can login now.")
            return redirect('login')
    return render(request, 'fyp/signup.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'fyp/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

from django.contrib.auth.decorators import login_required

from .models import UserProfile, Business, Event

@login_required
def dashboard_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    preferences = user_profile.preferences
    businesses = Business.objects.filter(category__in=preferences)
    events = Event.objects.filter(category__in=preferences)
    context = {
        'user_profile': user_profile,
        'businesses': businesses,
        'events': events
    }
    return render(request, 'fyp/dashboard.html', context)

def home_view(request):
    return render(request, 'fyp/home.html')
