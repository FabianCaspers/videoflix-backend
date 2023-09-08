from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer
from django.contrib.auth import authenticate, login as auth_login, logout
from django.views.decorators.csrf import csrf_exempt

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def user_login_view(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        username = email.split('@')[0]
        if not email or not password:
            return Response({'status': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return Response({'status': 'Logged in'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def logout_view(request):
    logout(request)
    return Response({'status': 'Logged out'}, status=status.HTTP_200_OK)