from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer
from django.contrib.auth import authenticate, login as auth_login, logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token


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
    email = request.data.get('email')
    password = request.data.get('password')
    username = email.split('@')[0]
    
    user = authenticate(request, username=username, password=password)

    if user is not None:
        auth_login(request, user)
        
        token, created = Token.objects.get_or_create(user=user)

        return Response({'status': 'Logged in', 'token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'status': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    user = request.user
    return Response({
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
    })


@api_view(['GET'])
def logout_view(request):
    logout(request)
    return Response({'status': 'Logged out'}, status=status.HTTP_200_OK)