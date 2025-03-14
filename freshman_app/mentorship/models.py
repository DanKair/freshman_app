from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class MentorshipRequest(models.Model):
    mentor = models.ForeignKey(User, related_name="mentor_requests", on_delete=models.CASCADE)
    mentee = models.ForeignKey(User, related_name="mentee_requests", on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=[("pending", "Pending"), ("accepted", "Accepted"), ("rejected", "Rejected")],
        default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("mentor", "mentee")

class Mentorship(models.Model):
    mentor = models.ForeignKey(User, related_name="mentors", on_delete=models.CASCADE)
    mentee = models.ForeignKey(User, related_name="mentees", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("mentor", "mentee")