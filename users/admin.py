from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'is_email_verified', 'is_approved', 'is_active', 'date_joined')
    list_filter = ('is_email_verified', 'is_active', 'is_staff', 'user_type', 'is_approved')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)
    
    fieldsets = (
        *UserAdmin.fieldsets,
        ('Account Status', {
            'fields': ('is_email_verified', 'is_approved', 'user_type'),
        }),
    )
    
    actions = ['approve_users', 'unapprove_users', 'verify_email', 'unverify_email']
    
    def approve_users(self, request, queryset):
        queryset.update(is_approved=True, is_active=True)
    approve_users.short_description = "Approve selected users"
    
    def unapprove_users(self, request, queryset):
        queryset.update(is_approved=False, is_active=False)
    unapprove_users.short_description = "Unapprove selected users"
    
    def verify_email(self, request, queryset):
        queryset.update(is_email_verified=True, is_active=True)
    verify_email.short_description = "Mark selected users as email verified"
    
    def unverify_email(self, request, queryset):
        queryset.update(is_email_verified=False, is_active=False)
    unverify_email.short_description = "Mark selected users as email unverified"

admin.site.register(User, CustomUserAdmin)