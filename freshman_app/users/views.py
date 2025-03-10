from django.contrib.auth import logout
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, FreshmanProfile, MentorProfile, ApplicantProfile
from .permissions import IsApplicant, IsFreshman, IsMentor
from .serializers import UserSerializer, UserRegisterSerializer, UserLoginSerializer, \
    ComplexRegisterSerializer, FreshmanSerializer, MentorSerializer, ApplicantSerializer, LogoutSerializer


# Create your views here.
# General Register for User model
class UserRegisterView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = serializer.data
        return Response(data, status=status.HTTP_201_CREATED)


class UserLoginView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class UserInfoView(APIView):
    # permission class is set to [IsAuthenticated] by default
    def get(self, request):
        user = request.user
        serializer = UserRegisterSerializer(user)
        return Response(serializer.data)



class ComplexRegisterView(GenericAPIView):
    serializer_class = ComplexRegisterSerializer
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class MentorProfileView(GenericAPIView):
    serializer_class = MentorSerializer
    permission_classes = [IsMentor]

    def get(self, request):
        """Get the authenticated user's mentor profile"""
        try:
            mentor_profile = request.user.mentor_profile
        except MentorProfile.DoesNotExist:
            return Response({"error": "Mentor profile not found"}, status=404)

        serializer = self.get_serializer(mentor_profile)
        return Response(serializer.data)

    def put(self, request):
        """Update the authenticated user's mentor profile"""
        try:
            mentor_profile = request.user.mentor_profile
        except MentorProfile.DoesNotExist:
            return Response({"error": "Mentor profile not found"}, status=404)

        serializer = self.get_serializer(mentor_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class ApplicantProfileView(GenericAPIView):
    permission_classes = [IsApplicant]
    serializer_class = ApplicantSerializer

    def get(self, request):
        """Get the authenticated user's applicant profile"""
        if not hasattr(request.user, 'applicant_profile'):
            return Response({"error": "Applicant profile not found"}, status=404)

        applicant_profile = request.user.applicant_profile
        serializer = self.get_serializer(applicant_profile)
        return Response(serializer.data)

    def put(self, request):
        """Update the authenticated user's applicant profile"""
        try:
            applicant_profile = request.user.applicant_profile
        except ApplicantProfile.DoesNotExist:
            return Response({"error": "Applicant profile not found"}, status=404)

        serializer = self.get_serializer(applicant_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class FreshmanProfileView(GenericAPIView):
    permission_classes = [IsFreshman]
    serializer_class = FreshmanSerializer
    def get(self, request):
        """Get the authenticated user's freshman profile"""
        if not hasattr(request.user, 'freshman_profile'):
            return Response({"error": "Freshman profile not found"}, status=404)

        freshman_profile = request.user.freshman_profile
        serializer = self.get_serializer(freshman_profile)
        return Response(serializer.data)

    def put(self, request):
        """Update the authenticated user's freshman profile"""
        if not hasattr(request.user, 'freshman_profile'):
            return Response({"error": "Freshman profile not found"}, status=404)

        freshman_profile = request.user.freshman_profile
        serializer = self.get_serializer(freshman_profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)


class UserLogoutView(APIView):
    """ View for user logout (session-based) """
    def post(self, request):
        serializer = LogoutSerializer(data={}, context={"request": request})
        serializer.save()
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)


# The rest lines of code made just for testing purposes

class FreshmenListAPIView(APIView):
    def get(self, request):
        user = FreshmanProfile.objects.all()
        serializer = FreshmanSerializer(user, many=True)
        return Response(serializer.data)



@api_view(["GET"])
def get_users(request):
    user = User.objects.all()
    serializer = UserSerializer(user, many=True)
    return Response(serializer.data)


