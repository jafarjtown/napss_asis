# Generated by Django 3.2 on 2024-07-07 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20240707_1802'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='time',
            options={'ordering': ['index']},
        ),
        migrations.AddField(
            model_name='lecturehour',
            name='venue',
            field=models.CharField(default='NFY', max_length=20),
        ),
    ]
