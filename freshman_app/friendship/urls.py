from django.urls import path
from . import views

urlpatterns = [
    path('send-request/', views.SendFriendRequestView.as_view(), name='send-friend-request'),
    path('respond-request/', views.RespondFriendRequestView.as_view(), name='respond-friend-request'),
    path('list/', views.ListFriendsView.as_view(), name='list-friends'),
    path('find-by-interest/', views.FindFriendsByInterestView.as_view(), name='find-friends-by-interest'),
    path('find-by-major/', views.FindFriendsByMajorView.as_view(), name='find-friends-by-interest'),
    path('remove-friend/', views.RemoveFriendView.as_view()),
]
