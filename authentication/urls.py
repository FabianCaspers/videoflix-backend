from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login_view, name='login'),
    path('current_user/', views.get_current_user, name='current-user'),
    path('confirm/<str:uidb64>/<str:token>/', views.confirm_email, name='confirm-email'),

]
