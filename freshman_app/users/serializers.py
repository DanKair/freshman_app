from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate, login, logout
from rest_framework.exceptions import ValidationError
from django.apps import apps

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

    """
    This line of code responsible for UserProfile Management
    I was lazy to create seperate UserProfile Serializer to handle this 
    That's why I just added method to already existing Serializer with same attributes :P
    """
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance



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

        return({"message": "Login succesfully completed✔!"})


class LogoutSerializer(serializers.Serializer):
    """ Serializer for user logout """

    def save(self, **kwargs):
        request = self.context.get('request')
        logout(request)  # Ends session


class ComplexRegisterSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, required=True)

    # Role-specific fields (optional at first)
    expertise_subject = serializers.CharField(required=False) #mentor related
    experience_years = serializers.IntegerField(required=False)
    year_of_study = serializers.IntegerField(required=False)
    faculty = serializers.CharField(required=False)
    is_available = serializers.BooleanField(required=False)

    high_school = serializers.CharField(required=False) # applicant related
    gpa = serializers.FloatField(required=False)
    intended_major = serializers.CharField(required=False)

    major = serializers.CharField(required=False) # freshman related
    enrolled_courses = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'phone_number', 'role',
                  'expertise_subject', 'year_of_study', 'is_available', 'faculty', 'experience_years',
                  'major', 'enrolled_courses', 'high_school', 'gpa', 'intended_major']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        role = data.get('role')

        # Ensure required fields are provided for each role
        if role == 'mentor':
            if not data.get('expertise_subject') or not data.get('year_of_study'):
                raise serializers.ValidationError("Mentors must provide expertise and year of study.")
        elif role == 'applicant':
            if not data.get('high_school') or not data.get('gpa') or not data.get('intended_major'):
                raise serializers.ValidationError("Applicants must provide high school name, GPA and intended major.")
        elif role == 'freshman':
            if not data.get('major'):
                raise serializers.ValidationError("Freshmen must provide major.")

        return data

    def create(self, validated_data):
        role = validated_data.pop('role')

        # Extract profile-related data
        mentor_data = {k: validated_data.pop(k) for k in ['expertise_subject', 'experience_years', 'year_of_study', 'is_available', 'faculty'] if k in validated_data}
        applicant_data = {k: validated_data.pop(k) for k in ['high_school', 'gpa', 'intended_major'] if k in validated_data}
        freshman_data = {k: validated_data.pop(k) for k in ['enrolled_courses', 'major'] if k in validated_data}

        # Create user
        user = User.objects.create_user(role=role, **validated_data)

        # Create corresponding profile
        if role == 'mentor':
            # This import was made to fix circular import issue
            MentorProfile = apps.get_model('profiles', 'MentorProfile')
            MentorProfile.objects.create(user=user, **mentor_data)
        elif role == 'applicant':
            # This import was made to fix circular import issue
            ApplicantProfile = apps.get_model('profiles', 'ApplicantProfile')
            ApplicantProfile.objects.create(user=user, **applicant_data)
        elif role == 'freshman':
            # This import was made to fix circular import issue
            FreshmanProfile = apps.get_model('profiles', 'FreshmanProfile')
            FreshmanProfile.objects.create(user=user, **freshman_data)

        return user


