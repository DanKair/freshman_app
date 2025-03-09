from django.contrib import admin
from .models import User, MentorProfile, FreshmanProfile, ApplicantProfile
# Register your models here.
admin.site.register(User)
admin.site.register(ApplicantProfile)
admin.site.register(FreshmanProfile)
admin.site.register(MentorProfile)