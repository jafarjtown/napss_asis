# Generated by Django 3.2 on 2024-07-07 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20240707_1534'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='time',
            name='am_pm',
        ),
        migrations.RemoveField(
            model_name='time',
            name='hour',
        ),
        migrations.RemoveField(
            model_name='time',
            name='minute',
        ),
        migrations.AddField(
            model_name='time',
            name='time',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
    ]
