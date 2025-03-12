from django.urls import path
from . import views

urlpatterns = [
    path('request-mentor', views.RequestMentorshipView.as_view()),
    path('respond-mentor', views.RespondMentorshipRequestView.as_view()),
    path('search-mentors/', views.SearchMentorsView.as_view(), name='search-mentors'),
    path('assign-mentor/', views.AssignMentorView.as_view(), name='assign-mentor'),
]
