from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['firstname','lastname', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            firstname= validated_data['firstname'],
            lastname= validated_data['lastname'],
            email = validated_data['email'],
            username = validated_data['username'],

        )
        user.set_password(validated_data['password'])# This hashes the password
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError('Invalid login credentials')
        if not user.is_active:
            raise serializers.ValidationError('User is inactive.')

        return {
            'email': user.email,
            'username': user.username,
            'message':'Login successful'
        }

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('firstname', 'lastname', 'username', 'email', 'password')

    def validate_email(self,value):
        return value.lower()

    def update(self, instance, validated_data):
    # Update user details (exclude password from being auto-updated)
        instance.firstname = validated_data.get('firstname', instance.firstname)
        instance.lastname = validated_data.get('lastname', instance.lastname)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)

    # Update password
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
