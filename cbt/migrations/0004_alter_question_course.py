# Generated by Django 3.2 on 2024-08-27 00:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0002_delete_newsletter'),
        ('cbt', '0003_question_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='objectives', to='material.course'),
        ),
    ]
