from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.serializers import UserSerializer, UserWithTokenSerializer
from authentication.models import User


class RetrieveUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        '''
        Get user by their token and return user data
        '''

        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class CreateUserView(APIView):
    '''
    Accept only POST requests
    Create new user based on submitted email, username and password
    '''
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        serializer = UserWithTokenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
