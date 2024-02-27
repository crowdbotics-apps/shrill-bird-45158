# urls.py
from django.urls import path
from .views import LoanCalculatorAPIView

urlpatterns = [
    path('calculate_loan/', LoanCalculatorAPIView.as_view(), name='calculate_loan'),
]
