from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate, login
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import ApplicantProfile, FreshmanProfile, MentorProfile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    # This serializer is generally for User model which has common fields
    # For different UserProfiles (Mentor, Freshman, Applicant)
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', "phone_number", 'role' ]
        read_only_fields = ('email', 'first_name', 'last_name')


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', "phone_number", 'role', 'password']
        # We add additional serializer field like model field
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')


        if username == "admin":
            raise ValidationError("Username can't be name like that")
        while "@example.com" in email:
            raise ValidationError("this email can't be accepted")

        return data


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        request = self.context.get('request')
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)

        if user is None:
            raise ValidationError("Invalid email or password")

        login(request, user)

        return({"message": "Login succesfully completed!"})













"""class ApplicantRegisterSerializer(serializers.ModelSerializer):
    gpa = serializers.FloatField(required=True)
    intended_major = serializers.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', "phone_number", 'password', 'gpa', 'intended_major']
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        gpa = validated_data.pop('gpa')  # Extract GPA
        password = validated_data.pop('password')

        user = User.objects.create_user(**validated_data, role='applicant')
        user.set_password(password)
        user.save()

        ApplicantProfile.objects.create(user=user, gpa=gpa)  # Create profile

        return user"""


