"""
URL configuration for inventory project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from users import views as user_views
from users.forms import CustomPasswordResetForm
from . import views

# Customize admin site
admin.site.site_url = '/home/'  # Add this line to change "View site" link

urlpatterns = [
    # Root URL now redirects to login
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('admin/login/', auth_views.LoginView.as_view(
        template_name='admin/login.html',
        redirect_authenticated_user=True
    ), name='admin_login'),
    path('signup/', user_views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('verify-email/<uidb64>/<token>/', 
         user_views.verify_email, name='verify_email'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset.html',
             form_class=CustomPasswordResetForm,
             email_template_name='users/password_reset_email.html',
             subject_template_name='users/password_reset_subject.txt'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    
    # Main URLs - now home is at /home
    path('home/', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('vet/', include('vet_supplies.urls')),
    path('office/', include('office_supplies.urls')),
    path('reports/', include('reports.urls')),  # Changed from TemplateView to include reports URLs
    path('mass-outgoing/', views.MassOutgoingListView.as_view(), name='mass-outgoing-list'),
    path('', include('users.urls')),  # Add this if not already present
]