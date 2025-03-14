from django.urls import path
from . import views
urlpatterns = [
    path("register/v1/", views.UserRegisterView.as_view(), name="This one only related to User Model"),
    path('register/v2/', views.ComplexRegisterView.as_view(), name="Use this endpoint as main sign-up feature"),
    path('login/', views.UserLoginView.as_view(), name="User Login using email and password to authenticate into system"),
    path('logout/', views.UserLogoutView.as_view(), name="User Logout function, make sure to pass blank fields"),
    path('profile/', views.UserProfileView.as_view(), name="Get User Model related info for current user"),
    path('users/', views.get_users, name="Get list of all users"),
]