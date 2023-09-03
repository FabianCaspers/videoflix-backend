from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='email', read_only=True)
    class Meta:
        model = User
        fields = ['id', 'password', 'first_name', 'last_name', 'email', 'username']
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        email = validated_data.get('email')
        username = email.split('@')[0] 
        user = User(username=username, **validated_data)
        user.set_password(password)
        user.save()
        return user
