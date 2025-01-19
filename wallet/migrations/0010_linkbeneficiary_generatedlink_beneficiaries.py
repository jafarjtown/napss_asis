# Generated by Django 5.1.3 on 2025-01-19 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0009_alter_generatedlink_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='LinkBeneficiary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='generatedlink',
            name='beneficiaries',
            field=models.ManyToManyField(blank=True, to='wallet.linkbeneficiary'),
        ),
    ]
