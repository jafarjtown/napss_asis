# Generated by Django 5.1.3 on 2025-01-15 20:59

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0008_generatedlink'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generatedlink',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]