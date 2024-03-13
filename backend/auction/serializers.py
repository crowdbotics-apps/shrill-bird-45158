from rest_framework import serializers
from vehicle.serializers import VehicleListSerializer
from .models import Auction, Bid

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = '__all__'


class AuctionSerializer(serializers.ModelSerializer):
    bids = serializers.SerializerMethodField()
    vehicle = VehicleListSerializer()
    class Meta:
        model = Auction
        fields = '__all__'
    
    def get_bids(self, obj):
        bids = obj.bid_set.all().order_by('-amount').first()
        return BidSerializer(instance=[bids], many=True).data
    
    def get_vehicle(self, obj):
        vehicle = obj.vehicle
        return VehicleListSerializer(instance=vehicle).data



