from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from profiles.permissions import IsFreshman, IsMentor
from .models import Mentorship, MentorshipRequest
from .serializers import MentorshipRequestSerializer
from profiles.models import FreshmanProfile, MentorProfile
from profiles.serializers import MentorProfileSerializer


class RequestMentorshipView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        mentor_id = request.data.get("mentor")
        if not mentor_id:
            return Response({"error": "Mentor ID is required"}, status=400)

        if MentorshipRequest.objects.filter(mentee=request.user, mentor_id=mentor_id).exists():
            return Response({"error": "Mentorship request already sent"}, status=400)

        mentorship_request = MentorshipRequest.objects.create(mentee=request.user, mentor_id=mentor_id)
        return Response(MentorshipRequestSerializer(mentorship_request).data, status=201)


class RespondMentorshipRequestView(APIView):
    permission_classes = [IsMentor]

    def post(self, request, *args, **kwargs):
        request_id = request.data.get("request_id")
        action = request.data.get("action")

        mentorship_request = get_object_or_404(MentorshipRequest, id=request_id, mentor=request.user)

        if action == "accept":
            Mentorship.objects.create(mentor=mentorship_request.mentor, mentee=mentorship_request.mentee)
            mentorship_request.status = "accepted"
        elif action == "reject":
            mentorship_request.status = "rejected"
        else:
            return Response({"error": "Invalid action"}, status=400)

        mentorship_request.save()
        return Response(MentorshipRequestSerializer(mentorship_request).data, status=200)


class ListMentorsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        mentors = MentorProfile.objects.filter(availability=True)
        return Response(MentorProfileSerializer(mentors, many=True).data)


class SearchMentorsView(APIView):
    permission_classes = [IsFreshman]

    def get(self, request, *args, **kwargs):
        expertise_query = request.query_params.get("expertise_subject", "").strip().lower()
        if not expertise_query:
            return Response({"error": "Expertise query is required"}, status=400)

        mentors = MentorProfile.objects.filter(expertise_subject__icontains=expertise_query)
        return Response(MentorProfileSerializer(mentors, many=True).data, status=200)


class AssignMentorView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        mentor_id = request.data.get("mentor_id")
        if not mentor_id:
            return Response({"error": "Mentor ID is required"}, status=400)

        mentor = get_object_or_404(MentorProfile, user_id=mentor_id)
        freshman_profile = get_object_or_404(FreshmanProfile, user=request.user)

        freshman_profile.mentor = mentor
        freshman_profile.save()

        return Response({"message": "Mentor assigned successfully!"})


class ViewMentorView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        mentorship = Mentorship.objects.filter(mentee=request.user, status="accepted").first()

        if not mentorship:
            return Response({"error": "No mentor assigned"}, status=404)

        return Response(MentorProfileSerializer(mentorship.mentor).data)