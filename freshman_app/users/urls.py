from django.urls import path
from . import views
urlpatterns = [
    path("register/v1/", views.UserRegisterView.as_view()),
    path('register/v2/', views.ComplexRegisterView.as_view()),
    path('login/', views.UserLoginView.as_view()),
    path('logout/', views.UserLogoutView.as_view()),
    path('profile/mentor/', views.MentorProfileView.as_view()),
    path('profile/freshman/', views.FreshmanProfileView.as_view()),
    path('profile/applicant/', views.ApplicantProfileView.as_view()),
    path('users/', views.get_users),
    path('me/', views.UserInfoView.as_view(), name="Get User Model related info for current user"),
    path('freshmans/', views.FreshmenListAPIView.as_view()),
]