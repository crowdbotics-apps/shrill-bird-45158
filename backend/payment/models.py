from django.db import models

# Create your models here.
class Payment(models.Model):
    acution = models.ForeignKey('auction.Auction', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    buyer = models.ForeignKey('users.User', on_delete=models.CASCADE)
    payment_date = models.DateTimeField()
    payment_method = models.CharField(max_length=20, choices=[('credit_card','credit_card'),('paypal','paypal')])
    status = models.CharField(max_length=20, default='pending', choices=[('pending','pending'),('completed','completed'),('failed','failed'),('refunded','refunded')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('auction', 'buyer')

    def __str__(self):
        return self.payer.name
    
    def save(self, *args, **kwargs):
        if self.status == 'completed':
            self.acution.status = 'completed'
            self.acution.save()
        super().save(*args, **kwargs)
    
    
    
# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LoanCalculatorSerializer
from decimal import Decimal

class LoanCalculatorAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoanCalculatorSerializer(data=request.data)
        if serializer.is_valid():
            vehicle_price = serializer.validated_data['vehicle_price']
            down_payment = serializer.validated_data['down_payment']
            loan_term = serializer.validated_data['loan_term']
            interest_rate = serializer.validated_data['interest_rate']
            
            loan_amount = vehicle_price - down_payment
            monthly_interest_rate = interest_rate / 100 / 12
            monthly_payment = (loan_amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -loan_term)
            
            return Response({'monthly_payment': round(monthly_payment, 2)})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
