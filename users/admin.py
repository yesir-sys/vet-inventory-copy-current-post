from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'is_email_verified', 'is_active', 'date_joined')
    list_filter = ('is_email_verified', 'is_active', 'is_staff', 'user_type')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)
    
    fieldsets = (
        *UserAdmin.fieldsets,
        ('Account Status', {
            'fields': ('is_email_verified', 'user_type'),
        }),
    )
    
    actions = ['verify_email', 'unverify_email']
    
    def verify_email(self, request, queryset):
        queryset.update(is_email_verified=True, is_active=True)
    verify_email.short_description = "Mark selected users as email verified"
    
    def unverify_email(self, request, queryset):
        queryset.update(is_email_verified=False, is_active=False)
    unverify_email.short_description = "Mark selected users as email unverified"

admin.site.register(User, CustomUserAdmin)