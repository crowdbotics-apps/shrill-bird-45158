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
