# Generated by Django 5.1.6 on 2025-03-21 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('admin', 'Admin'), ('staff', 'Staff'), ('user', 'User')], default='user', max_length=10),
        ),
    ]
