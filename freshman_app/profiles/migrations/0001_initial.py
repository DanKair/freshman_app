# Generated by Django 5.1.6 on 2025-03-12 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicantProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('high_school', models.CharField(max_length=255)),
                ('gpa', models.DecimalField(decimal_places=2, max_digits=5)),
                ('intended_major', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='FreshmanProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('major', models.CharField(max_length=255)),
                ('enrolled_courses', models.TextField(blank=True, help_text='List of courses enrolled in')),
            ],
        ),
        migrations.CreateModel(
            name='MentorProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year_of_study', models.IntegerField()),
                ('faculty', models.CharField(max_length=100, verbose_name='Факультет')),
                ('expertise_subject', models.TextField(help_text='Subjects or areas they mentor in')),
                ('is_available', models.BooleanField()),
            ],
        ),
    ]
