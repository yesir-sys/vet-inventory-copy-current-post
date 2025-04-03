from django.db import connection
from django.contrib.sessions.models import Session
from django.utils import timezone
import datetime

class ConnectionCleanupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        connection.close_if_unusable_or_obsolete()
        return response

class SessionCleanupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Clean expired sessions
        Session.objects.filter(expire_date__lt=timezone.now()).delete()
        
        response = self.get_response(request)
        
        # Ensure session is saved
        if hasattr(request, 'session'):
            request.session.save()
            
        return response

    def process_request(self, request):
        if hasattr(request, 'session') and not request.session.session_key:
            request.session.save()
            request.session.modified = True

        return None

class SessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.session.session_key:
            request.session.create()
            
        response = self.get_response(request)
        
        if hasattr(request, 'session'):
            request.session.save()
            
        return response