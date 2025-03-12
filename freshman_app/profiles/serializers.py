from rest_framework import serializers
from .models import FreshmanProfile, ApplicantProfile, MentorProfile

class FreshmanSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True) # to see username instead of id
    class Meta:
        model = FreshmanProfile
        fields = ['user', 'major', 'enrolled_courses', 'interests']



class MentorSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True) # to see username instead of id
    class Meta:
        model = MentorProfile
        fields = '__all__'


class ApplicantSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True) # to see username instead of id
    class Meta:
        model = ApplicantProfile
        fields = '__all__'