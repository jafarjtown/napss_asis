# Generated by Django 5.1.3 on 2025-01-13 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServicePriority',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=35)),
                ('level', models.IntegerField(default=0)),
                ('information', models.TextField()),
            ],
        ),
    ]
