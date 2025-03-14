from django.contrib import admin
from .models import ApplicantProfile, FreshmanProfile, MentorProfile
# Register your models here.
admin.site.register(ApplicantProfile)
admin.site.register(FreshmanProfile)
admin.site.register(MentorProfile)