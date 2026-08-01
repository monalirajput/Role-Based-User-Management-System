from django.urls import path
from . import views
from django.contrib.auth import logout
from django.shortcuts import redirect

urlpatterns = [
    path('', views.user_login, name='login'),
    path('register/', views.register, name='register'),

    path('superadmin-dashboard/', views.superadmin_dashboard, name='superadmin_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('user-packages/', views.user_packages, name='user_packages'),
    path('notifications/', views.notifications_view, name='notifications'),
    
]
