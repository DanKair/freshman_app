from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import MentorProfile, FreshmanProfile, ApplicantProfile
from .serializers import MentorProfileSerializer, ApplicantProfileSerializer, FreshmanProfileSerializer
from .permissions import IsFreshman, IsMentor, IsApplicant
# Profile Management system based on roles

class MentorProfileView(GenericAPIView):
    serializer_class = MentorProfileSerializer
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
    serializer_class = ApplicantProfileSerializer

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
    serializer_class = FreshmanProfileSerializer
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



# Test views
class FreshmenListAPIView(APIView):
    def get(self, request):
        freshman = FreshmanProfile.objects.all()
        serializer = FreshmanProfileSerializer(freshman, many=True)
        return Response(serializer.data)

class MentorListAPIView(APIView):
    def get(self, request):
        mentor = MentorProfile.objects.all()
        serializer = MentorProfileSerializer(mentor, many=True)
        return Response(serializer.data)

class ApplicantListAPIView(APIView):
    def get(self, request):
        applicant = ApplicantProfile.objects.all()
        serializer = ApplicantProfileSerializer(applicant, many=True)
        return Response(serializer.data)



class GetMentorProfileView(APIView):
    def get(self, request, pk):
        mentor = MentorProfile.objects.get(id=pk)
        serializer = MentorProfileSerializer(mentor)
        return Response(serializer.data)


