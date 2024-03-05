from django.urls import path

from users.views import (
    user_redirect_view,
    user_update_view,
    user_detail_view,
)
from .views import PhoneLoginView, VerifyCodeAPIView, PasswordResetView, PasswordResetConfirmView, UniqueUsernameCheck,UserProfileView

app_name = "users"
urlpatterns = [
    path('unique-username/', UniqueUsernameCheck.as_view(), name='unique-user'),
    path('phone-login/', PhoneLoginView.as_view()),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    # path("~update/", view=user_update_view, name="update"),
    # path("<str:username>/", view=user_detail_view, name="detail"),
    path('verify/', VerifyCodeAPIView.as_view(), name='verify'),
    path(
        "forgot-password/",
        PasswordResetView.as_view(),
        name="forgot-password",
    ),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm_api'),
]
