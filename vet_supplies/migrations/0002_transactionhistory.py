# Generated by Django 5.1.6 on 2025-03-21 08:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vet_supplies', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('IN', 'Stock In'), ('OUT', 'Stock Out'), ('ADJ', 'Adjustment'), ('EXP', 'Expired')], max_length=3)),
                ('quantity', models.IntegerField()),
                ('previous_quantity', models.IntegerField()),
                ('new_quantity', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('notes', models.TextField(blank=True)),
                ('reference_id', models.CharField(blank=True, max_length=100)),
                ('supply', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vet_supplies.vetsupply')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]
