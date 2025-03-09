from django.urls import path
from . import views
urlpatterns = [
    path("register/", views.UserRegisterView.as_view()),
    path('login/', views.UserLoginView.as_view()),
    path('users/', views.get_users),
]