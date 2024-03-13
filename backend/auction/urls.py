from django.urls import path

from django.views.generic import TemplateView
urlpatterns = [
    path('live-auction/', TemplateView.as_view(template_name='live_auction.html')),
]