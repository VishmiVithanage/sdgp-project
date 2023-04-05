from django.shortcuts import render

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from .serializers import ProcessImageSerializer

class ProcessImageView(CreateAPIView):
    serializer_class = ProcessImageSerializer
    permission_classes = [AllowAny]