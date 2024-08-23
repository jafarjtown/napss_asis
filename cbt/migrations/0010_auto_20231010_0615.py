# Generated by Django 3.2 on 2023-10-10 05:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cbt', '0009_fillintheblanksquestion_truefalsecourse_truefalsequestion'),
    ]

    operations = [
        migrations.CreateModel(
            name='FillInTheBlank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='fillintheblanksquestion',
            name='question_text',
        ),
        migrations.AddField(
            model_name='fillintheblanksquestion',
            name='course',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='cbt.fillintheblank'),
            preserve_default=False,
        ),
    ]
