# Generated by Django 5.1.3 on 2024-12-25 15:19

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_blogpage_allow_comment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogcomment',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
