from rest_framework import serializers
from .models import MentorshipRequest, Mentorship

class MentorshipRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorshipRequest
        fields = ['id', 'mentor', 'mentee', 'status', 'created_at']
        read_only_fields = ['mentor', 'status', 'created_at']

class MentorshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentorship
        fields = ['id', 'mentor', 'mentee', 'created_at']
