from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import FriendRequest, Friendship
from .serializers import FriendRequestSerializer, FriendshipSerializer
from django.shortcuts import get_object_or_404

from profiles.models import FreshmanProfile, ApplicantProfile
from profiles.serializers import FreshmanProfileSerializer, ApplicantProfileSerializer \


class SendFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        receiver_id = request.data.get("receiver")
        if not receiver_id:
            return Response({"error": "Receiver ID is required"}, status=400)

        if FriendRequest.objects.filter(sender=request.user, receiver_id=receiver_id).exists():
            return Response({"error": "Friend request already sent"}, status=400)

        friend_request = FriendRequest.objects.create(sender=request.user, receiver_id=receiver_id)
        return Response(FriendRequestSerializer(friend_request).data, status=201)


class RespondFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request_id = request.data.get("request_id")
        action = request.data.get("action")  # "accept" or "reject"

        friend_request = get_object_or_404(FriendRequest, id=request_id, receiver=request.user)

        if action == "accept":
            Friendship.objects.create(user1=friend_request.sender, user2=friend_request.receiver)
            friend_request.status = "accepted"
        elif action == "reject":
            friend_request.status = "rejected"
        else:
            return Response({"error": "Invalid action"}, status=400)

        friend_request.save()
        return Response(FriendRequestSerializer(friend_request).data, status=200)


class ListFriendsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        friends = Friendship.objects.filter(user1=request.user).union(
            Friendship.objects.filter(user2=request.user)
        )
        return Response(FriendshipSerializer(friends, many=True).data)


class FindFriendsByInterestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        interest_query = request.query_params.get("interest", "").strip().lower()
        if not interest_query:
            return Response({"error": "Interest query is required"}, status=400)

        # Search in FreshmanProfiles
        freshman_matches = FreshmanProfile.objects.filter(interests__icontains=interest_query)
        # Search in ApplicantProfiles
        applicant_matches = ApplicantProfile.objects.filter(interests__icontains=interest_query)

        # Combine results
        results = {
            "freshmen": FreshmanProfileSerializer(freshman_matches, many=True).data,
            "applicants": ApplicantProfileSerializer(applicant_matches, many=True).data,
        }
        return Response(results, status=200)

class RemoveFriendView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        friend_id = request.data.get("friend_id")
        if not friend_id:
            return Response({"error": "Friend ID is required"}, status=400)

        # Check if a friendship exists between the user and the friend
        friendship = Friendship.objects.filter(
            (Q(user1=request.user) & Q(user2_id=friend_id)) | (Q(user1_id=friend_id) & Q(user2=request.user))
        ).first()

        if not friendship:
            return Response({"error": "Friendship does not exist"}, status=404)

        friendship.delete()
        return Response({"message": "Friend removed successfully!"}, status=200)