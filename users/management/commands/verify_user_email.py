from django.core.management.base import BaseCommand
from users.models import User

class Command(BaseCommand):
    help = 'Verify email for a user'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email to verify')

    def handle(self, *args, **kwargs):
        email = kwargs['email']
        try:
            user = User.objects.get(email=email)
            user.is_email_verified = True
            user.is_active = True
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f'Successfully verified email for user: {user.username}')
            )
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'No user found with email: {email}')
            )
