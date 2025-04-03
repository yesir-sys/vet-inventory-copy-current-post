from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import PermissionDenied

class ApprovalBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = super().authenticate(request, username=username, password=password, **kwargs)
            if user:
                # Skip verification checks for superusers and staff
                if user.is_superuser or user.is_staff:
                    return user
                    
                # Regular user checks
                if not user.is_email_verified:
                    raise PermissionDenied("Please verify your email address before logging in.")
                if not user.is_approved:
                    raise PermissionDenied("Your account is awaiting administrator approval.")
                if not user.is_active:
                    raise PermissionDenied("Your account has been deactivated. Please contact the administrator.")
            return user
        except PermissionDenied as e:
            raise e
        except Exception:
            return None
