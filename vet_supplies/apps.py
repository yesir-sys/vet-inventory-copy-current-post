from django.apps import AppConfig

class VetSuppliesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vet_supplies'
    verbose_name = 'Veterinary Supplies'

    def ready(self):
        import reports.signals  # Import the signals