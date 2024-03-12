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