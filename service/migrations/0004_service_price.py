# Generated by Django 5.1.3 on 2025-01-13 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_service_priority'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]
