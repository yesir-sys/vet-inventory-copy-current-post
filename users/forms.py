from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'username'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'email'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'new-password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'new-password'
        })

class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your email address',
            'autocomplete': 'email'
        })

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("There is no user registered with this email address.")
        return email

    def send_mail(self, subject_template_name, email_template_name,
                 context, from_email, to_email, html_email_template_name=None):
        """Override to send HTML email"""
        try:
            email = self.cleaned_data.get('email', '')
            context['user'] = User.objects.get(email=email)
            
            from django.core.mail import EmailMultiAlternatives
            from django.template import loader
            
            subject = loader.render_to_string(subject_template_name, context)
            subject = ''.join(subject.splitlines())  # Remove newlines
            body = loader.render_to_string(email_template_name, context)
            
            email_message = EmailMultiAlternatives(
                subject,
                body,
                from_email,
                [to_email]
            )
            email_message.content_subtype = 'html'
            email_message.send()
            
            print(f"Password reset email sent successfully to {to_email}")
        except Exception as e:
            print(f"Failed to send password reset email: {str(e)}")
            raise