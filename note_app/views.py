# users/views.py
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from django.shortcuts import render
from .serializers import UserSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer



