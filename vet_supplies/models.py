from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db.models import Q, F
from django.contrib.auth import get_user_model
import random
import string

User = get_user_model()


# VetCategory Model
class VetCategory(models.Model):
    name = models.CharField(
        max_length=100, 
        unique=True,
        error_messages={'unique': 'This category already exists.'}
    )
    description = models.TextField(blank=True, default="")
    alert_threshold = models.PositiveIntegerField(
        default=0,
        help_text="Minimum quantity to trigger alerts (0 to disable)"
    )

    class Meta:
        verbose_name_plural = "Vet Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


# VetSupply Model
class VetSupply(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# VetSupply Model
class VetSupply(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        VetCategory, 
        on_delete=models.CASCADE,
        related_name="supplies"
    )
    quantity = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    reorder_level = models.PositiveIntegerField(
        default=10,
        validators=[MinValueValidator(1)]
    )
    last_updated = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)
    expiration_date = models.DateField(
        null=True, 
        blank=True,
        verbose_name="Expiration Date (optional)"
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Vet Supplies"
        ordering = ['-last_updated']
        constraints = [
            models.CheckConstraint(
                check=models.Q(quantity__gte=0),
                name="vet_supply_quantity_positive"
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.category})"

    def get_absolute_url(self):
        return reverse('vet-supply-detail', kwargs={'pk': self.pk})
    
    @property
    def needs_reorder(self):
        return self.quantity <= self.reorder_level
    
    @property
    def expiration_status(self):
        if not self.expiration_date:
            return 'non-expiring'
            
        today = timezone.now().date()
        delta = (self.expiration_date - today).days
        
        if delta < 0:
            return 'expired'
        if delta <= 7:
            return 'critical'
        if delta <= 30:
            return 'warning'
        return 'ok'

    def clean(self):
        if self.expiration_date and self.expiration_date < timezone.now().date():
            raise ValidationError({
                'expiration_date': 'Expiration date cannot be in the past'
            })
        
        if self.reorder_level >= 1000:
            raise ValidationError({
                'reorder_level': 'Reorder level is unrealistically high (max 999)'
            })
        
        if self.quantity < 0:
            raise ValidationError({
                'quantity': 'Quantity cannot be negative'
            })

    def save(self, *args, **kwargs):
        # Check if expiration_date is in the past
        if self.expiration_date and self.expiration_date < timezone.now().date():
            self.expiration_date = None  # or handle it as needed
        self.full_clean()
        super().save(*args, **kwargs)
        
    def delete_if_expired(self):
        if self.expiration_status == 'expired':
            self.is_active = False
            self.save()


# ExpiredItem Model
class ExpiredItem(models.Model):
    supply = models.ForeignKey(VetSupply, on_delete=models.CASCADE)
    expiration_date = models.DateField()


# Notification Model
class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('low_stock', 'Low Stock'),
        ('expiring', 'Expiring Soon'),
        ('expired', 'Expired'),
        ('out_of_stock', 'Out of Stock'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='vet_notifications'
    )
    supply = models.ForeignKey(
        'VetSupply',
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    resolved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Inventory Notification'
        verbose_name_plural = 'Inventory Notifications'

    def __str__(self):
        return f"{self.get_notification_type_display()} - {self.supply.name}"

    @classmethod
    def create_alert(cls, supply, notification_type):
        """Create notifications for relevant users"""
        users = User.objects.filter(
            Q(is_superuser=True) |
            Q(groups__name='Inventory Managers')
        ).distinct()

        for user in users:
            cls.objects.get_or_create(
                user=user,
                supply=supply,
                notification_type=notification_type,
                defaults={
                    'message': cls.generate_message(supply, notification_type),
                    'resolved': False
                }
            )

    @classmethod
    def generate_message(cls, supply, notification_type):
        """Generate context-aware messages"""
        # Check for expiration_date being None
        if notification_type in ['expiring', 'expired'] and not supply.expiration_date:
            return f"{supply.name} has no expiration date specified."

        messages = {
            'low_stock': (
                f"Low stock alert for {supply.name}. "
                f"Current quantity: {supply.quantity} "
                f"(Reorder level: {supply.reorder_level})"
            ),
            'expiring': (
                f"{supply.name} expires on {supply.expiration_date.strftime('%Y-%m-%d')}. "
                f"Quantity affected: {supply.quantity}"
            ),
            'expired': (
                f"{supply.name} expired on {supply.expiration_date.strftime('%Y-%m-%d')}. "
                f"Quantity affected: {supply.quantity}"
            ),
            'out_of_stock': f"{supply.name} is out of stock!"
        }

        return messages.get(notification_type, "Inventory Alert")


# OfficeCategory Model
class OfficeCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# OfficeSupply Model
class OfficeSupply(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(OfficeCategory, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    reorder_level = models.PositiveIntegerField(default=10)
    expiration_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)  # Added is_active field

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(quantity__gte=0),
                name='vet_supplies_quantity_positive'
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.category})"

    def get_absolute_url(self):
        return reverse('office-supply-detail', kwargs={'pk': self.pk})

    @property
    def needs_reorder(self):
        return self.quantity <= self.reorder_level

    @property
    def expiration_status(self):
        if not self.expiration_date:
            return 'non-expiring'

        today = timezone.now().date()
        delta = (self.expiration_date - today).days

        if delta < 0:
            return 'expired'
        if delta <= 7:
            return 'critical'
        if delta <= 30:
            return 'warning'
        return 'ok'

    def clean(self):
        """Combined validation rules"""
        if self.expiration_date and self.expiration_date < timezone.now().date():
            raise ValidationError({
                'expiration_date': 'Expiration date cannot be in the past'
            })

        if self.reorder_level >= 1000:
            raise ValidationError({
                'reorder_level': 'Reorder level is unrealistically high (max 999)'
            })

        if self.quantity < 0:
            raise ValidationError({
                'quantity': 'Quantity cannot be negative'
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def delete_if_expired(self):
        if self.expiration_status == 'expired':
            self.is_active = False
            self.save()


# StockMovement Model
class StockMovement(models.Model):
    supply = models.ForeignKey(VetSupply, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    movement_type = models.CharField(max_length=10, choices=[('in', 'In'), ('out', 'Out')])
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)


# Remove or comment out the Treatment model if it exists
# class Treatment(models.Model):
#     ...

# Remove or comment out the TransactionHistory model
# class TransactionHistory(models.Model):
#     ...


class VetSupplyTransaction(models.Model):
    processed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )


'''
class MassOutgoing(models.Model):
    # ...existing MassOutgoing model code...

class MassOutgoingItem(models.Model):
    # ...existing MassOutgoingItem model code...

class MassOutgoingTransaction(models.Model):
    # ...existing MassOutgoingTransaction model code...

class MassOutgoingTransactionItem(models.Model):
    # ...existing MassOutgoingTransactionItem model code...
'''

class TransactionHistory(models.Model):
    TRANSACTION_TYPES = [
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
        ('ADJ', 'Adjustment'),
        ('EXP', 'Expired')
    ]
    
    supply = models.ForeignKey('VetSupply', on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=3, choices=TRANSACTION_TYPES)
    quantity = models.IntegerField()
    previous_quantity = models.IntegerField()
    new_quantity = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    reference_id = models.CharField(max_length=100, blank=True)
    processed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = 'Transaction Histories'
        ordering = ['-timestamp']


class InventoryMovement(models.Model):
    MOVEMENT_TYPES = [
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
        ('ADJ', 'Adjustment'),
        ('DEL', 'Deleted'),
        ('EDT', 'Edited'),
        ('EXP', 'Expired')
    ]
    # ...existing code...
