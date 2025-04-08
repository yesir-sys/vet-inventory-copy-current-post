from django.apps import AppConfig

class OfficeSuppliesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'office_supplies'
    verbose_name = 'Office Supplies'

    def ready(self):
        import reports.signals  # Import the signals