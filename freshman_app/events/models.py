from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.

class EventCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    date = models.DateTimeField()
    max_attendees = models.PositiveIntegerField()
    category = models.ForeignKey(EventCategory, on_delete=models.SET_NULL, null=True, blank=True)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name="hosted_events")
    attendees = models.ManyToManyField(User, through="EventRSVP", related_name="joined_events")

    def __str__(self):
        return self.title


class EventRSVP(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[("going", "Going"), ("not_going", "Not Going")])

    class Meta:
        unique_together = ("event", "user")

    def __str__(self):
        return f"{self.user} - {self.event.title} ({self.status})"


