# Generated by Django 5.0 on 2024-06-30 21:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_material_course_alter_pastquestion_year'),
        ('cbt', '0010_auto_20231010_0615'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='essaytest',
            name='questions',
        ),
        migrations.RemoveField(
            model_name='fillintheblanksquestion',
            name='course',
        ),
        migrations.RemoveField(
            model_name='truefalsequestion',
            name='course',
        ),
        migrations.CreateModel(
            name='CourseCBT',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cbt_test', to='app.course')),
                ('essays', models.ManyToManyField(blank=True, to='cbt.essayquestion')),
                ('fill_the_blank', models.ManyToManyField(blank=True, to='cbt.fillintheblanksquestion')),
                ('objectives', models.ManyToManyField(blank=True, to='cbt.question')),
                ('true_false', models.ManyToManyField(blank=True, to='cbt.truefalsequestion')),
            ],
        ),
        migrations.DeleteModel(
            name='Course',
        ),
        migrations.DeleteModel(
            name='EssayTest',
        ),
        migrations.DeleteModel(
            name='FillInTheBlank',
        ),
        migrations.DeleteModel(
            name='TrueFalseCourse',
        ),
    ]
