from datetime import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import VetSupply, Notification

@receiver(post_save, sender=VetSupply)
def create_supply_notifications(sender, instance, created, **kwargs):
    if not created:  # Only check existing supplies
        if instance.needs_reorder:
            Notification.objects.create(
                supply=instance,
                message=f"Low stock alert for {instance.name}",
                notification_type='LOW_STOCK',
                # Remove user reference since categories don't have users
            )
        
        if instance.expiration_status in ['critical', 'expired']:
            Notification.objects.create(
                supply=instance,
                message=f"Expiration alert for {instance.name}",
                notification_type='EXPIRATION',
                # Remove user reference since categories don't have users
            )