# Generated by Django 5.1.6 on 2025-03-12 08:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='applicantprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='applicant_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='freshmanprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='freshman_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='mentorprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='mentor_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
