from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from .serializers import EventSerializer, EventCategorySerializer
from .models import Event, EventRSVP, EventCategory
from users.serializers import UserSerializer

User = get_user_model()

# The first 3 main views responsible for CRUD operations towards Event model
class CreateEventView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(host=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class EditDeleteEventView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, event_id):
        event = get_object_or_404(Event, id=event_id, host=request.user)
        serializer = EventSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, event_id):
        event = get_object_or_404(Event, id=event_id, host=request.user)
        event.delete()
        return Response({"message": "Event deleted"}, status=204)

# Search events by title and description or get list of all events
class SearchListEventsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search_query = request.query_params.get("search", "").strip().lower()
        if search_query:
            events = Event.objects.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
        else:
            events = Event.objects.all()

        return Response(EventSerializer(events, many=True).data)


class RSVPEventView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        if event.attendees.count() >= event.max_attendees:
            return Response({"error": "Event is full"}, status=400)

        rsvp, created = EventRSVP.objects.get_or_create(event=event, user=request.user)
        rsvp.status = "going"
        rsvp.save()

        return Response({"message": "You are attending this event"}, status=200)


class CancelRSVPView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        rsvp = EventRSVP.objects.filter(event_id=event_id, user=request.user).first()
        if not rsvp:
            return Response({"error": "You are not attending this event"}, status=400)

        rsvp.delete()
        return Response({"message": "RSVP canceled"}, status=200)


class EventAttendeesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id):
        attendees = User.objects.filter(eventrsvp__event_id=event_id, eventrsvp__status="going")
        return Response(UserSerializer(attendees, many=True).data)


class UserEventsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        hosted_events = request.user.hosted_events.all()
        joined_events = request.user.joined_events.all()

        return Response({
            "hosted_events": EventSerializer(hosted_events, many=True).data,
            "joined_events": EventSerializer(joined_events, many=True).data
        })

# Events Categories Related Views

class ListCategoriesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        categories = EventCategory.objects.all()
        return Response(EventCategorySerializer(categories, many=True).data)


class ListEventsByCategoryView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, category_id):
        events = Event.objects.filter(category_id=category_id)
        return Response(EventSerializer(events, many=True).data)