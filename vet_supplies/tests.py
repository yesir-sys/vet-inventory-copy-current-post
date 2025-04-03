from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import VetSupply, VetCategory

class VetSupplyTests(TestCase):
    def setUp(self):
        self.category = VetCategory.objects.create(
            name="Test Category",
            description="Test Description",
            alert_threshold=5
        )
        
    def test_supply_creation(self):
        supply = VetSupply.objects.create(
            name="Test Supply",
            category=self.category,
            quantity=10,
            reorder_level=5
        )
        self.assertEqual(supply.name, "Test Supply")
        self.assertEqual(supply.quantity, 10)

    def test_negative_quantity(self):
        with self.assertRaises(ValidationError):
            VetSupply.objects.create(
                name="Invalid Supply",
                category=self.category,
                quantity=-1
            )
    
    def test_expiration_status(self):
        future_date = timezone.now().date() + timezone.timedelta(days=40)
        supply = VetSupply.objects.create(
            name="Expiring Supply",
            category=self.category,
            quantity=10,
            expiration_date=future_date
        )
        self.assertEqual(supply.expiration_status, 'ok')

    def test_needs_reorder(self):
        supply = VetSupply.objects.create(
            name="Low Stock Supply",
            category=self.category,
            quantity=5,
            reorder_level=10
        )
        self.assertTrue(supply.needs_reorder)
