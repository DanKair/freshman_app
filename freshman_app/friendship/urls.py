from django.urls import path
from .views import SendFriendRequestView, RespondFriendRequestView, ListFriendsView, FindFriendsByInterestView, \
    RemoveFriendView

urlpatterns = [
    path('send-request/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('respond-request/', RespondFriendRequestView.as_view(), name='respond-friend-request'),
    path('list/', ListFriendsView.as_view(), name='list-friends'),
    path('find-by-interest/', FindFriendsByInterestView.as_view(), name='find-friends-by-interest'),
    path('remove-friend/', RemoveFriendView.as_view())
]
