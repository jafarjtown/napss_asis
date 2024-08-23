# Generated by Django 5.0 on 2024-06-30 21:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_pastquestion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materials', to='app.course'),
        ),
        migrations.AlterField(
            model_name='pastquestion',
            name='year',
            field=models.DateField(),
        ),
    ]
