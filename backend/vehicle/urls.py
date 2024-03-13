from django.urls import path
from .views import VehicleAdd, VehicleList, EditVehicle, DeleteImage, DeleteVideo, GetVehicleAuctionStatus
urlpatterns = [
    path('add/', VehicleAdd.as_view(), name='vehicle-add'),
    path('list/', VehicleList.as_view(), name='vehicle-list'),
    path('edit/', EditVehicle.as_view(), name='vehicle-edit'),
    path('delete-image/', DeleteImage.as_view(), name='delete-image'),
    path('delete-video/', DeleteVideo.as_view(), name='delete-video'),
    path('get-vehicle-auction-status/', GetVehicleAuctionStatus.as_view(), name='get-vehicle-auction-status'),
]