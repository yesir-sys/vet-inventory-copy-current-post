from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
import random
import string
from django.utils import timezone

class InventoryMovement(models.Model):
    MOVEMENT_TYPES = (
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
        ('ADJ', 'Adjustment'),
        ('EDT', 'Edited'),
        ('DEL', 'Deleted'),
        ('EXP', 'Expired')
    )

    timestamp = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPES)
    quantity = models.IntegerField()
    previous_quantity = models.IntegerField(default=0)
    current_quantity = models.IntegerField(default=0)
    processed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-timestamp']

class StockLevel(models.Model):
    date = models.DateField()
    total_items = models.IntegerField()
    low_stock_items = models.IntegerField()
    expiring_soon_items = models.IntegerField()
    supply_type = models.CharField(max_length=10)  # 'vet' or 'office'

    class Meta:
        unique_together = ['date', 'supply_type']
