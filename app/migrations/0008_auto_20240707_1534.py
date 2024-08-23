# Generated by Django 3.2 on 2024-07-07 14:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_material_course_alter_pastquestion_year'),
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Time',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hour', models.CharField(max_length=2)),
                ('minute', models.CharField(max_length=2)),
                ('am_pm', models.CharField(max_length=2)),
            ],
        ),
        migrations.RemoveField(
            model_name='timetable',
            name='modified',
        ),
        migrations.RemoveField(
            model_name='timetable',
            name='original',
        ),
        migrations.CreateModel(
            name='LectureHour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.course')),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.day')),
                ('hour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.time')),
            ],
        ),
        migrations.AddField(
            model_name='timetable',
            name='lectures',
            field=models.ManyToManyField(blank=True, to='app.LectureHour'),
        ),
    ]
