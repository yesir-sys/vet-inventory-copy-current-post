from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from vet_supplies.models import VetSupply
from office_supplies.models import OfficeSupply
from .models import InventoryMovement
from django.contrib.auth import get_user_model
from django.apps import apps

def get_current_user():
    """Get current user if crum is available"""
    try:
        from crum import get_current_user
        return get_current_user()
    except ImportError:
        return None

def get_user_or_none():
    """Helper function to safely get current user"""
    try:
        user = get_current_user()
        return user if user and user.is_authenticated else None
    except:
        return None

@receiver([pre_save], sender=VetSupply)
@receiver([pre_save], sender=OfficeSupply)
def track_inventory_changes(sender, instance, **kwargs):
    try:
        if instance.pk:
            old_instance = sender.objects.get(pk=instance.pk)
            changes = []
            
            # Track field changes
            fields_to_track = ['name', 'category', 'quantity', 'reorder_level', 'expiration_date']
            for field in fields_to_track:
                old_value = getattr(old_instance, field)
                new_value = getattr(instance, field)
                if old_value != new_value:
                    changes.append(f"{field}: {old_value} → {new_value}")
            
            if changes:
                # Get current user from thread local storage or use None
                user = get_user_or_none()
                
                if old_instance.quantity != instance.quantity:
                    movement_type = 'ADJ'
                    quantity = abs(instance.quantity - old_instance.quantity)
                else:
                    movement_type = 'EDT'
                    quantity = 0
                    
                # Create movement record with user (can be None)
                InventoryMovement.objects.create(
                    content_type=ContentType.objects.get_for_model(instance),
                    object_id=instance.pk,
                    movement_type=movement_type,
                    quantity=quantity,
                    previous_quantity=old_instance.quantity,
                    current_quantity=instance.quantity,
                    processed_by=user,
                    notes=f"Edited: {', '.join(changes)}"
                )
    except sender.DoesNotExist:
        pass

@receiver([pre_delete], sender=VetSupply)
@receiver([pre_delete], sender=OfficeSupply)
def track_inventory_deletion(sender, instance, **kwargs):
    user = get_user_or_none()
    InventoryMovement.objects.create(
        content_type=ContentType.objects.get_for_model(instance),
        object_id=instance.pk,
        movement_type='DEL',
        quantity=instance.quantity,
        previous_quantity=instance.quantity,
        current_quantity=0,
        processed_by=user,
        notes=f"Item deleted: {instance.name}"
    )
