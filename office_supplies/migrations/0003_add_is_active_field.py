from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('office_supplies', '0002_officemassincoming'),  # Fixed dependency
    ]

    operations = [
        migrations.AddField(
            model_name='officesupply',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
