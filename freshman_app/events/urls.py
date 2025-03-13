from django.urls import path
from . import views


urlpatterns = [
    path("", views.SearchListEventsView.as_view(), name="search-events"),
    path("create/", views.CreateEventView.as_view(), name="create-event"),
    path("<int:event_id>/", views.EditDeleteEventView.as_view(), name="edit-delete-event"),
    path("<int:event_id>/rsvp/", views.RSVPEventView.as_view(), name="rsvp-event"),
    path("<int:event_id>/cancel/", views.CancelRSVPView.as_view(), name="cancel-rsvp"),
    path("<int:event_id>/attendees/", views.EventAttendeesView.as_view(), name="event-attendees"),
    path("my-events/", views.UserEventsView.as_view(), name="user-events"),
    path("categories/", views.ListCategoriesView.as_view(), name="list-categories"),
    path("categories/<int:category_id>/events/", views.ListEventsByCategoryView.as_view(), name="events-by-category"),
]