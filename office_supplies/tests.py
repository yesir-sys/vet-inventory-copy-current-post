from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import OfficeSupply, OfficeCategory

class OfficeSupplyTests(TestCase):
    def setUp(self):
        self.category = OfficeCategory.objects.create(name="Test Category")
        
    def test_supply_creation(self):
        supply = OfficeSupply.objects.create(
            name="Test Supply",
            category=self.category,
            quantity=10,
            reorder_level=5
        )
        self.assertEqual(supply.name, "Test Supply")
        self.assertEqual(supply.quantity, 10)
    
    def test_invalid_reorder_level(self):
        with self.assertRaises(ValidationError):
            OfficeSupply.objects.create(
                name="Invalid Supply",
                category=self.category,
                quantity=10,
                reorder_level=1000  # Should raise ValidationError
            )
    
    def test_expiration_date_validation(self):
        past_date = timezone.now().date() - timezone.timedelta(days=1)
        with self.assertRaises(ValidationError):
            OfficeSupply.objects.create(
                name="Expired Supply",
                category=self.category,
                quantity=10,
                expiration_date=past_date
            )
    
    def test_delete_if_expired(self):
        today = timezone.now().date()
        supply = OfficeSupply.objects.create(
            name="Expiring Supply",
            category=self.category,
            quantity=10,
            expiration_date=today
        )
        supply.delete_if_expired()
        self.assertFalse(supply.is_active)
