from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
User = get_user_model()

class ApplicantProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="applicant_profile")
    high_school = models.CharField(max_length=255)
    gpa = models.DecimalField(max_digits=5, decimal_places=2)
    intended_major = models.CharField(max_length=100)
    interests = models.TextField(blank=True, help_text="Comma-separated interests (e.g., Python, Chess, AI)")

    def __str__(self):
        return f"{self.user} from {self.high_school} with GPA: {self.gpa}"

    def get_interest_list(self):
        return [i.strip().lower() for i in self.interests.split(",") if i.strip()]



class MentorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mentor_profile')
    year_of_study = models.IntegerField()
    faculty = models.CharField(max_length=100, verbose_name="Факультет")
    experience_years = models.PositiveIntegerField()
    expertise_subject = models.TextField(help_text="Subjects or areas they mentor in")
    is_available = models.BooleanField()

    def __str__(self):
        return f"{self.user} - {self.faculty} - {self.expertise_subject}"

    def get_expertise_subject_list(self):
        return [e.strip().lower() for e in self.expertise_subject.split(",") if e.strip()]


class FreshmanProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="freshman_profile")
    major = models.CharField(max_length=255)
    enrolled_courses = models.TextField(blank=True, help_text="List of courses enrolled in")
    mentor = models.ForeignKey(MentorProfile, null=True, blank=True, on_delete=models.SET_NULL)


    def __str__(self):
        return f"{self.user} - {self.major}"

    interests = models.TextField(blank=True, help_text="Comma-separated interests (e.g., Python, Chess, AI)")

    def get_interest_list(self):
        return [i.strip().lower() for i in self.interests.split(",") if i.strip()]