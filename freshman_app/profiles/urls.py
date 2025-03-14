from django.urls import path
from . import views

urlpatterns = [
    path('mentor/', views.MentorProfileView.as_view()),
    path('freshman/', views.FreshmanProfileView.as_view()),
    path('applicant/', views.ApplicantProfileView.as_view()),
    path('list/freshmans/', views.FreshmenListAPIView.as_view()),
]