from django.core.serializers import get_serializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserSerializer, UserRegisterSerializer, UserLoginSerializer, \
    ComplexRegisterSerializer, LogoutSerializer


# Create your views here.
# General Register for User model
class UserRegisterView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = serializer.data
        return Response(data, status=status.HTTP_201_CREATED)


class UserLoginView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class ComplexRegisterView(GenericAPIView):
    serializer_class = ComplexRegisterSerializer
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserLogoutView(APIView):
    """ View for user logout (session-based) """
    def post(self, request):
        serializer = LogoutSerializer(data={}, context={"request": request})
        serializer.save()
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)


class UserProfileView(GenericAPIView):
    # permission class is set to [IsAuthenticated] by default
    serializer_class = UserRegisterSerializer
    def get(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def put(self, request):
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# The rest lines of code made just for testing purposes


@api_view(["GET"])
def get_users(request):
    user = User.objects.all()
    serializer = UserSerializer(user, many=True)
    return Response(serializer.data)


