from rest_framework import serializers
from .models import Vehicle, VehicleImage, VehicleVideo
import os
import boto3
from urllib.parse import urlparse
import environ
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_file = os.path.join(BASE_DIR, ".env")
env = environ.Env()

class VehicleImageSerializer(serializers.ModelSerializer):
    document_signed = serializers.SerializerMethodField()
    class Meta:
        model = VehicleImage
        fields = ['id', 'image', 'image_for', 'document_signed']

    def get_document_signed(self, obj):
        if obj.image:
            parsed_url = urlparse(obj.image.url)
            object_key = parsed_url.path[1:]
            # Generate a signed URL using the extracted object key
            s3 = boto3.client('s3',
                            region_name=env.str("AWS_STORAGE_REGION", ""),
                            config=boto3.session.Config(signature_version='s3v4'))
            expiration_time = 3600
            signed_url = s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': 'jonesy-energy-42233', 'Key': object_key},
                ExpiresIn=expiration_time
            )
            return signed_url
        else:
            return None
        


class VehicleVideoSerializer(serializers.ModelSerializer):
    document_signed = serializers.SerializerMethodField()
    class Meta:
        model = VehicleVideo
        fields = ['id', 'video', 'video_for', 'document_signed'] 

    def get_document_signed(self, obj):
        if obj.video:
            parsed_url = urlparse(obj.video.url)
            object_key = parsed_url.path[1:]
            # Generate a signed URL using the extracted object key
            s3 = boto3.client('s3',
                            region_name=env.str("AWS_STORAGE_REGION", ""),
                            config=boto3.session.Config(signature_version='s3v4'))
            expiration_time = 3600
            signed_url = s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': 'shrill-bird-45158', 'Key': object_key},
                ExpiresIn=expiration_time
            )
            return signed_url
        else:
            return None


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'user', 'name', 'description', 'price', 'make', 'model', 'year', 'reserve_price', 'mileage', 'vehicle_specifications', 'buy_now', 'status']

    def create(self, validated_data):
        images_data = self.context.get('request').FILES.getlist('images')
        videos_data = self.context.get('request').FILES.getlist('videos')
        vehicle = Vehicle.objects.create(**validated_data)
        for image_data in images_data:
            VehicleImage.objects.create(vehicle=vehicle, image=image_data)
        for video_data in videos_data:
            VehicleVideo.objects.create(vehicle=vehicle, video=video_data)
        return vehicle
    

class VehicleListSerializer(serializers.ModelSerializer):
    images = VehicleImageSerializer(many=True, read_only=True)
    videos = VehicleVideoSerializer(many=True, read_only=True)
    class Meta:
        model = Vehicle
        fields = '__all__'
        depth = 1
