from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class FriendRequest(models.Model):
    sender = models.ForeignKey(User, related_name="sent_requests", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_requests", on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=[("pending", "Pending"), ("accepted", "Accepted"), ("rejected", "Rejected")],
        default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("sender", "receiver")

class Friendship(models.Model):
    user1 = models.ForeignKey(User, related_name="friends1", on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name="friends2", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user1", "user2")
