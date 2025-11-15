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
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    preferences = user_profile.preferences
    businesses = Business.objects.filter(category__in=preferences)
    events = Event.objects.filter(category__in=preferences)
    context = {
        'user_profile': user_profile,
        'businesses': businesses,
        'events': events
    }
    return render(request, 'fyp/dashboard.html', context)

@login_required
def add_business_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category = request.POST.get('category')
        
        if not name or not description or not category:
            messages.error(request, "All fields are required.")
        else:
            Business.objects.create(
                name=name,
                description=description,
                category=category,
                owner=request.user
            )
            messages.success(request, "Business submitted for verification.")
            return redirect('dashboard')
            
    return render(request, 'fyp/add_business.html')

@login_required
def add_event_view(request):
    user_businesses = Business.objects.filter(owner=request.user)
    if not user_businesses:
        messages.error(request, "You must own a business to create an event.")
        return redirect('dashboard')

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category = request.POST.get('category')
        business_id = request.POST.get('business')

        if not name or not description or not category or not business_id:
            messages.error(request, "All fields are required.")
        else:
            try:
                business = Business.objects.get(id=business_id, owner=request.user)
                Event.objects.create(
                    name=name,
                    description=description,
                    category=category,
                    business=business
                )
                messages.success(request, "Event submitted successfully.")
                return redirect('dashboard')
            except Business.DoesNotExist:
                messages.error(request, "Invalid business selected.")

    context = {
        'user_businesses': user_businesses
    }
    return render(request, 'fyp/add_event.html', context)

from django.shortcuts import get_object_or_404
from .models import Business, Review, Event, UserProfile

@login_required
def business_detail_view(request, business_id):
    business = get_object_or_404(Business, id=business_id)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if not rating or not comment:
            messages.error(request, "Rating and comment are required.")
        else:
            if Review.objects.filter(business=business, user=request.user).exists():
                messages.error(request, "You have already reviewed this business.")
            else:
                Review.objects.create(
                    business=business,
                    user=request.user,
                    rating=rating,
                    comment=comment
                )
                messages.success(request, "Review submitted successfully.")
                return redirect('business_detail', business_id=business.id)

    reviews = business.reviews.all().order_by('-created_at')
    context = {
        'business': business,
        'reviews': reviews
    }
    return render(request, 'fyp/business_detail.html', context)

@login_required
def owner_dashboard_view(request):
    businesses = Business.objects.filter(owner=request.user)
    context = {
        'businesses': businesses
    }
    return render(request, 'fyp/owner_dashboard.html', context)

def home_view(request):
    return render(request, 'fyp/landingpage.html')
