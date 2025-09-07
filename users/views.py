from django.shortcuts import render

# Create your views here.
# users/views.py
from rest_framework import generics, permissions
from .serializers import UserRegisterSerializer, UserSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView

class ProfileView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
