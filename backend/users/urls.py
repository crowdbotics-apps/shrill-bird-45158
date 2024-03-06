from django.urls import path

from users.views import (
    user_redirect_view,
    user_update_view,
    user_detail_view,
)
from .views import SendOTPView, PhoneLoginView, VerifyCodeAPIView, PasswordResetView, PasswordResetConfirmView, UniqueUsernameCheck,UserProfileView,DeleteUserByPhone, Login, SignupwithEmailAndUsername, UserOnboardingView, UserStripeToken

app_name = "users"
urlpatterns = [
    path('unique-username/', UniqueUsernameCheck.as_view(), name='unique-user'),
    path('send-otp/', SendOTPView.as_view()),
    path('phone-login/', PhoneLoginView.as_view()),
    path('onboarding/', UserOnboardingView.as_view(), name='onboarding'),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    # path("~update/", view=user_update_view, name="update"),
    # path("<str:username>/", view=user_detail_view, name="detail"),
    path('confirm-otp/', VerifyCodeAPIView.as_view(), name='verify'),
    path(
        "forgot-password/",
        PasswordResetView.as_view(),
        name="forgot-password",
    ),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm_api'),
    path('delete-user/', DeleteUserByPhone.as_view(), name='delete-user'),
    path('login/', Login.as_view(), name='login'),
    path('username-signup/', SignupwithEmailAndUsername.as_view(), name='signup'),
    path('custom_token/', UserStripeToken.as_view(), name='stripe'),
]
