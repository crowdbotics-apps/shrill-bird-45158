from django.shortcuts import render
from rest_framework.views import APIView
from .models import Vehicle, VehicleImage, VehicleVideo
from .serializers import VehicleSerializer, VehicleListSerializer
from rest_framework.response import Response
from rest_framework import status
import json
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser , JSONParser, FileUploadParser
from rest_framework.response import Response
from rest_framework import status
from auction.models import Bid
# Create your views here.


class VehicleAdd(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser, FileUploadParser]
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def post(self, request):
        data = request.POST.get('data', None)
        data = json.loads(data)
        data['user'] = request.user.id
        serializer = VehicleSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class VehicleList(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request):
        vehicles = Vehicle.objects.filter(user=request.user)
        serializer = VehicleListSerializer(vehicles, many=True)
        return Response(serializer.data)
    

class EditVehicle(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def put(self, request):
        data = request.POST.get('data', None)
        data = json.loads(data)
        data['user'] = request.user.id
        id = data.pop('id')
        if not id:
            return Response({'error': 'id is required'}, status=status.HTTP_400_BAD_REQUEST)
        vehicle = Vehicle.objects.get(id=id)
        serializer = VehicleSerializer(vehicle, data=data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DeleteImage(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def post(self, request):
        id = request.data.get('id', None)
        if not id:
            return Response({'error': 'id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            image = VehicleImage.objects.get(id=id)
            image.delete()
            return Response({'message': 'Image deleted successfully'}, status=status.HTTP_200_OK)
        except VehicleImage.DoesNotExist:
            return Response({'error': 'Image not found'}, status=status.HTTP_400_BAD_REQUEST)
        

class DeleteVideo(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def post(self, request):
        id = request.data.get('id', None)
        if not id:
            return Response({'error': 'id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            video = VehicleVideo.objects.get(id=id)
            video.delete()
            return Response({'message': 'Video deleted successfully'}, status=status.HTTP_200_OK)
        except VehicleVideo.DoesNotExist:
            return Response({'error': 'Video not found'}, status=status.HTTP_400_BAD_REQUEST)
    
    
class GetVehicleAuctionStatus(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request):
        vehicle_id = request.GET.get('id', None)
        if not vehicle_id:
            return Response({'error': 'id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        vehicle = Vehicle.objects.get(id=vehicle_id)
        
        # Get the count of bids for the vehicle
        num_bids = Bid.objects.filter(vehicle=vehicle).count()
        
        auction_status = {
            'highest_bid': vehicle.highest_bid,
            'num_bids': num_bids,
            'reserve_price': vehicle.reserve_price,
            'auction_end_date': vehicle.auction_end_date,
            'time_remaining': vehicle.time_remaining_in_auction()
        }
        
        return Response({'auction_status': auction_status})

