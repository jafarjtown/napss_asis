# Generated by Django 3.2 on 2024-08-27 00:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0002_delete_newsletter'),
        ('cbt', '0002_auto_20240827_0054'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='course',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='objectives', to='material.course'),
            preserve_default=False,
        ),
    ]
