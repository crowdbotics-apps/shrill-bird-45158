from django.db import models
from datetime import datetime
from django.utils import timezone
from auction.models import Auction

# Create your models here.

class Vehicle(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    reserve_price = models.DecimalField(max_digits=10, decimal_places=2)
    mileage = models.IntegerField()
    vehicle_specifications = models.TextField()
    buy_now = models.BooleanField(default=False)
    status = models.CharField(max_length=20, default='available', choices=[('available','available'),('sold','sold')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

    def time_remaining_in_auction(self):
        auction = Auction.objects.filter(vehicle=self).first()
        if auction:
            end_date = auction.end_date
            now = timezone.now()
            time_remaining = end_date - now
            return time_remaining
        return None
    
    
class VehicleImage(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='vehicle_images/')
    image_for = models.CharField(max_length=20, default='vehicle', choices=[('vehicle','vehicle'),('thumbnail','thumbnail'),('report','report')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vehicle.name
    
class VehicleVideo(models.Model):    
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='videos')
    video = models.FileField(upload_to='vehicle_videos/')
    video_for = models.CharField(max_length=20, default='vehicle', choices=[('vehicle','vehicle'),('thumbnail','thumbnail')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vehicle.name