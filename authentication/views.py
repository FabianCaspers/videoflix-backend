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
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponseRedirect, HttpResponse
from .models import UserProfile
from django.db.models.signals import post_save
from django.dispatch import receiver

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            mail_subject = 'Bestätigen Sie Ihre E-Mail-Adresse.'
            message = (f"Bitte klicken Sie auf den folgenden Link, um Ihre E-Mail zu bestätigen und Ihren Account zu aktivieren. "
                       f"Nach der Aktivierung werden Sie automatisch zur Login-Seite weitergeleitet: "
                       f"https://fabianvideoflix.pythonanywhere.com/confirm?uid={uid}&token={token}")
            
            send_mail(mail_subject, message, 'fabian.caspers1308@gmail.com', [user.email], fail_silently=False)
            
            return Response({"status": "success", "message": "Registrierung erfolgreich. Bitte überprüfen Sie Ihre E-Mail, um Ihre Registrierung zu bestätigen."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def confirm_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)

        if default_token_generator.check_token(user, token):
            print("Token is valid")
            user.is_active = True
            user.save()

            user_profile = UserProfile.objects.get(user=user)
            user_profile.is_verified = True
            user_profile.save()

            return Response({"status": "success", "message": "E-Mail-Bestätigung erfolgreich."}, status=status.HTTP_200_OK)
        else:
            return HttpResponse('Der Aktivierungslink ist ungültig!')

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return HttpResponse('Der Aktivierungslink ist ungültig!')


@api_view(['POST'])
def user_login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    username = email.split('@')[0]

    user = authenticate(request, username=username, password=password)

    if user is not None:
        user_profile = UserProfile.objects.get(user=user)
        if user_profile.is_verified:
            auth_login(request, user)
            
            token, created = Token.objects.get_or_create(user=user)

            return Response({'status': 'Logged in', 'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Account not verified'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'status': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

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