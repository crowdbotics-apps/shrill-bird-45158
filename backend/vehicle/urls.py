from django.urls import path
from .views import VehicleAdd, VehicleList

urlpatterns = [
    path('add/', VehicleAdd.as_view(), name='vehicle-add'),
    path('list/', VehicleList.as_view(), name='vehicle-list'),
]