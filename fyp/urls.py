from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'), 
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('add_business/', views.add_business_view, name='add_business'),
    path('add_event/', views.add_event_view, name='add_event'),
    path('business/<int:business_id>/', views.business_detail_view, name='business_detail'),
    path('owner/dashboard/', views.owner_dashboard_view, name='owner_dashboard'),
    path('', views.home_view, name='home'),
]
