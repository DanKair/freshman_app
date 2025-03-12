from django.urls import path
from . import views
urlpatterns = [
    path("register/v1/", views.UserRegisterView.as_view()),
    path('register/v2/', views.ComplexRegisterView.as_view()),
    path('login/', views.UserLoginView.as_view()),
    path('logout/', views.UserLogoutView.as_view()),
    path('users/', views.get_users),
    path('profile/', views.UserProfileView.as_view(), name="Get User Model related info for current user"),
]