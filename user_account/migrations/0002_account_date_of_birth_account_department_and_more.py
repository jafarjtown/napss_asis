# Generated by Django 5.1.3 on 2025-02-22 21:52

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0002_department_active_material_download_count'),
        ('user_account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='date_of_birth',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='account',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='material.department'),
        ),
        migrations.AddField(
            model_name='account',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='M', max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='account',
            name='phone_number',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='account',
            name='profile_pic',
            field=models.FileField(default="img/default.png", upload_to='profile'),
            preserve_default=False,
        ),
    ]
