from django.urls import path

from users.views import (
    user_redirect_view,
    user_update_view,
    user_detail_view,
)
from .views import SignUpView, VerifyCodeAPIView, PasswordResetView, PasswordResetConfirmView

app_name = "users"
urlpatterns = [
    path('phone-login/', SignUpView.as_view()),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    # path("~update/", view=user_update_view, name="update"),
    # path("<str:username>/", view=user_detail_view, name="detail"),
    path('verify/', VerifyCodeAPIView.as_view(), name='verify'),
    path(
        "forgot-password/",
        PasswordResetView.as_view(),
        name="forgot-password",
    ),
    path('/password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm_api'),
]
