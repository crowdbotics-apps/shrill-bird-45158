from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, UpdateView
from .models import User
from .utils import send_verification_code
from rest_framework.generics import CreateAPIView
from .serializers import PhoneSignupSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer
import os
from shrill_bird_45158.utiles import brevo_email_send
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import User
from .serializers import VerificationSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import VerificationSerializer


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




class SignUpView(CreateAPIView):
    serializer_class = PhoneSignupSerializer

    def perform_create(self, serializer):
        phone_number = self.request.data.get('phone_number')
        user, created = User.objects.get_or_create(phone_number=phone_number, username=phone_number)
        if created:
            send_verification_code(user)



class VerifyCodeAPIView(generics.GenericAPIView):
    serializer_class = VerificationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data.get('phone_number')
        verification_code = serializer.validated_data.get('verification_code')
        try:
            user = User.objects.get(phone_number=phone_number)
            if user.verify_code(verification_code):
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid verification code'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)



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
