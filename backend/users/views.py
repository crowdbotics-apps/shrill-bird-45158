from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, UpdateView
from .models import User, UserVehiclesReminder
from .utils import send_verification_code
from rest_framework.generics import CreateAPIView
from .serializers import PhoneSignupSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer
import os
from shrill_bird_45158.utiles import brevo_email_send
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import VerificationSerializer
from home.api.v1.serializers import SignupSerializer

from rest_framework.response import Response
from rest_framework import status
from .serializers import PhoneSignupSerializer
from .utils import send_verification_code
from .serializers import UserProfileSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ["name"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()



import random

def generate_verification_code():
    # Generate a random 6-digit numeric code
    return ''.join(random.choices('0123456789', k=6))

class PhoneLoginView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        try:
            user = User.objects.get(phone_number=phone_number)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

class SendOTPView(APIView):
    def post(self, request):
        serializer = PhoneSignupSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data.get('phone_number')
            verification_code = generate_verification_code()
            try:
                output = send_verification_code(phone_number, verification_code)
                print("output", output)
                if output.account_sid:
                    response_data = {'detail': 'Verification code sent successfully.',
                                     'verification_code': verification_code}
                    return Response(response_data, status=status.HTTP_200_OK)
            except Exception as e:
                print("error", e)
                return Response({'detail': 'Failed to send verification code.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeAPIView(generics.GenericAPIView):
    serializer_class = VerificationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data.get('phone_number')
        check_phone = User.objects.filter(phone_number=phone_number)
        if check_phone.exists():
            return Response({'detail': 'Phone number already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = User.objects.create(phone_number=phone_number)
            token = Token.objects.create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)

class PasswordResetView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'detail': 'User not found with this email.'}, status=status.HTTP_400_BAD_REQUEST)

            uid = urlsafe_base64_encode(force_text(user.pk).encode())
            token = default_token_generator.make_token(user)
            frontend = os.environ.get("FRONTEND_URL")
            reset_url = f"{frontend}/password/reset/{uid}/{token}/"
            link = f'Click the following link to reset your password: {reset_url}'
            msg = render_to_string(
                "email/resetpassword.html",
                {"link": reset_url,
                "site_url": os.environ.get("SITE_URL")},
            )
            to = [
                    {
                    "email": user.email,
                    "name": user.username
                    }
                ]
            emailsend = brevo_email_send(to=to, subject="Forgot Password", htmlContent=msg, textContent="Hello")
            return Response({'detail': 'Password reset link sent to your email.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PasswordResetConfirmView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            uid = serializer.validated_data['uid']
            token = serializer.validated_data['token']
            password = serializer.validated_data['password']

            try:
                uid = force_text(urlsafe_base64_decode(uid))
                user = User.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None

            if user and default_token_generator.check_token(user, token):
                user.set_password(password)
                user.save()
                
                return Response({'detail': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid UID or token.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UniqueUsernameCheck(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        try:
            if username:
                user = User.objects.get(username=username)
                return Response({'detail': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'detail': 'Username is required.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'detail': 'Username is unique.'}, status=status.HTTP_200_OK)
        

class DeleteUserByPhone(APIView):
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        try:
            user = User.objects.get(phone_number=phone_number)
            user.delete()
            return Response({'detail': 'User deleted successfully.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'detail': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        

class Login(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid password.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'detail': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': 'Invalid username.'}, status=status.HTTP_400_BAD_REQUEST)
        


class SignupwithEmailAndUsername(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Profile updated successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, *args, **kwargs):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'updated successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return Response({'detail': 'User deleted successfully.'}, status=status.HTTP_200_OK)

from .serializers import UserStripeSerializer
class UserOnboardingView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def post(self, request):
        try:
            makeandmodel = request.data.get('makeandmodel')
            username = request.data.get('username')
            phone_number = request.data.get('phone_number')
            user = request.user
            if makeandmodel:
                for item in makeandmodel:
                    make = item.get('make')
                    model = item.get('model')
                    if make and model:
                        UserVehiclesReminder.objects.create(user=user, make=make, model=model)
            if username and phone_number:
                user.username = username
                user.phone_number = phone_number
                user.save()
            return Response({'detail': 'Onboarding data saved successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': 'Failed to save onboarding data.'}, status=status.HTTP_400_BAD_REQUEST)
        

import stripe

class UserStripeView(APIView):
    def post(self, request, *args, **kwargs):
        stripe.api_key = "sk_test_51OlcTwHMwXjMgTe66E5ftR7biZPzZ73UiKuOPteujebBSqMJE6dVMeOISWv91eG4MXelX4nvzCRKJJRsMbrAvwgX000BhxToWb"
        customer = stripe.Customer.create(
            name="JyRosen")
        print("customer", customer.id)
        return Response({'detail': 'Stripe customer created successfully.'}, status=status.HTTP_200_OK)


from .models import UserStripe

class UserStripeToken(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def post(self, request, *args, **kwargs):
        stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
        custom_token = request.data.get('custom_token')
        if custom_token:
            user = request.user
            customer = stripe.Customer.create(
                name=user.username)
            UserStripe.objects.create(user=user, custom_token=custom_token, customer_id=customer.id)
            return Response({'detail': 'Stripe token created successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Custom token is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            user_stripe = UserStripe.objects.filter(user=user)
            serializer = UserStripeSerializer(user_stripe, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserStripe.DoesNotExist:
            return Response({'detail': 'User stripe does not exist.'}, status=status.HTTP_404_NOT_FOUND)
