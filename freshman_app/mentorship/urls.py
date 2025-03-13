from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.ListMentorsView.as_view()),
    path('request-mentor', views.RequestMentorshipView.as_view()),
    path('respond-mentor', views.RespondMentorshipRequestView.as_view()),
    path('search-mentors/', views.SearchMentorsView.as_view(), name='search-mentors'),
    path('assign-mentor/', views.AssignMentorView.as_view(), name='assign-mentor'),
    path('assigned-mentor/', views.ViewMentorView.as_view(), name="See your assigned mentor"),
]
