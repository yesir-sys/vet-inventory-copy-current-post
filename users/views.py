from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from .forms import CustomUserCreationForm
from .models import User
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.is_email_verified = False
            user.is_approved = True  # Automatically approve users
            user.save()
            send_verification_email(request, user)
            return render(request, 'users/verification_waiting.html')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

def send_verification_email(request, user):
    try:
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        domain = get_current_site(request).domain
        protocol = 'https' if request.is_secure() else 'http'
        
        mail_subject = 'Activate your account'
        message = render_to_string('users/verification_email.html', {
            'user': user,
            'domain': domain,
            'uid': uid,
            'token': token,
            'protocol': protocol,
        })
        
        print(f"Attempting to send email...")
        print(f"To: {user.email}")
        print(f"From: {settings.DEFAULT_FROM_EMAIL}")
        print(f"Host: {settings.EMAIL_HOST}")
        
        email = EmailMessage(
            subject=mail_subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        email.content_subtype = 'html'
        email.send(fail_silently=False)
        print("Email sent successfully!")
        
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        print(f"SMTP Settings:")
        print(f"Host: {settings.EMAIL_HOST}")
        print(f"Port: {settings.EMAIL_PORT}")
        print(f"TLS: {settings.EMAIL_USE_TLS}")
        print(f"User: {settings.EMAIL_HOST_USER}")
        user.is_active = True
        user.is_email_verified = True
        user.save()
        messages.warning(request, f'Email sending failed ({str(e)}). Account has been activated.')

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_email_verified = True
        user.is_active = True  # Activate user immediately after email verification
        user.save()
        messages.success(request, 'Your email has been verified. You can now login to your account.')
    else:
        messages.error(request, 'Activation link is invalid or has expired!')
    
    return redirect('login')

@method_decorator(ensure_csrf_cookie, name='dispatch')
class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        # Don't reuse existing session
        if not request.session.session_key:
            request.session.create()
        request.session.modified = True

    def get(self, request, *args, **kwargs):
        # Always generate new CSRF token
        request.META["CSRF_COOKIE_USED"] = True
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Generate new session key for each login
        request.session.cycle_key()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        
        try:
            user = User.objects.get(username=username)
            # Skip verification checks for admin/staff users
            if not user.is_staff and not user.is_superuser:
                if not user.is_email_verified:
                    messages.error(self.request, "Your email address has not been verified.")
                    return render(self.request, 'users/verification_waiting.html')
                if not user.is_approved:
                    messages.error(self.request, "Your account is pending administrator approval.")
                    return render(self.request, 'users/approval_pending.html')
        except User.DoesNotExist:
            messages.error(self.request, "No account found with this username.")
            return self.form_invalid(form)

        user = authenticate(self.request, username=username, password=password)
        if user is None:
            messages.error(self.request, "Invalid password.")
            return self.form_invalid(form)

        return super().form_valid(form)

    def form_invalid(self, form):
        for error in form.non_field_errors():
            messages.error(self.request, error)
        return super().form_invalid(form)

@login_required
@require_http_methods(["POST"])
def logout_view(request):
    """Handle user logout with CSRF verification"""
    try:
        logout(request)
        return JsonResponse({
            'success': True, 
            'redirect_url': reverse('login')
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)