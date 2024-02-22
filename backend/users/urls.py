from django.urls import path

from users.views import (
    user_redirect_view,
    user_update_view,
    user_detail_view,
)
from .views import SignUpView, VerifyCodeAPIView

app_name = "users"
urlpatterns = [
    path('phone-login/', SignUpView.as_view()),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    # path("~update/", view=user_update_view, name="update"),
    # path("<str:username>/", view=user_detail_view, name="detail"),
    path('verify/', VerifyCodeAPIView.as_view(), name='verify'),
]
