from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventorymovement',
            name='previous_quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='inventorymovement',
            name='current_quantity',
            field=models.IntegerField(default=0),
        ),
    ]
