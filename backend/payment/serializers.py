# serializers.py
from rest_framework import serializers

class LoanCalculatorSerializer(serializers.Serializer):
    vehicle_price = serializers.DecimalField(min_value=0, max_digits=10, decimal_places=2)
    down_payment = serializers.DecimalField(min_value=0, max_digits=10, decimal_places=2)
    loan_term = serializers.IntegerField(min_value=1)
    interest_rate = serializers.DecimalField(min_value=0, max_digits=5, decimal_places=2)
