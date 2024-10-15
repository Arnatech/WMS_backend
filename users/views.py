from allauth.socialaccount.signals import social_account_added
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UpdateUserSerializer
from .models import User
from django.db import IntegrityError
from .utils import send_user_notification_email
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user_model


class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                #Sending the welcome email
                subject = "Welcome to Aquaverse!"
                message = f"Hello Mr {user.firstname}, thank you for joining the Aquaverse family"
                send_user_notification_email(subject, message, user.email)

                return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({"error": "A user with this email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=serializer.validated_data['email'])
            refresh = RefreshToken.for_user(user)
            return Response({
                'email': user.email,
                'username': user.username,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'message': 'Login Successful'
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = UpdateUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            instance = serializer.save()

            #Sending profile update email
            subject = "Profile Updated Successfully"
            message = f"Hello {instance.firstname}, your account details have been successfully updated"
            send_user_notification_email(subject, message, instance.email)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SocialLoginView(APIView):
    def post(self, request):
        provider = request.data.get('provider')
        email = request.data.get('email')

        #Check if a social account already exists for this email
        try:
            social_account = SocialAccount.objects.get(provider=provider, uid=email)
            user = social_account.user
        except SocialAccount.DoesNotExist:
            #If not, create a new user
            user, created = User.objects.get_or_create(email=email)
            if created:
                user.firstname = request.data.get('firstname', '')
                user.lastname = request.data.get('lastname', '')
                user.username = request.data.get('username', '')
                user.save()

                #Create a social account entry to link user with specified provider and email
                SocialAccount.objects.create(user=user, provider=provider, uid=email)

        #Generate JWT token for the user
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'Social Login successful'
        }, status=status.HTTP_200_OK
        )