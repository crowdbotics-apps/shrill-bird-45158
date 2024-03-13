from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import logging
logger = logging.getLogger(__name__)

delivery_status_choices=[('undelivered','undelivered'),
                        ('delivered','delivered')
                        ]

auction_status_choices=[('open','open'),
                        ('running','running'),
                        ('cancelled','cancelled'),
                        ('paused','paused'),
                        ('completed','completed')
                        ]

# Create your models here.
class Auction(models.Model):
    countdown = models.IntegerField(default=0)
    highest_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_status = models.CharField(max_length=20, choices=delivery_status_choices, default='undelivered')
    buyer = models.ForeignKey('users.User', related_name='buyer', on_delete=models.CASCADE, null=True, blank=True)
    seller = models.ForeignKey('users.User', related_name='seller', on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=auction_status_choices, default='open')
    auctioned = models.BooleanField(default=False)
    vehicle = models.ForeignKey('vehicle.Vehicle', on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bidder = models.ForeignKey('users.User', on_delete=models.CASCADE)
    won = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
        
    def save(self, *args, **kwargs):
        if self.won:
            if self.amount > self.auction.highest_bid:
                self.auction.highest_bid = self.amount
                self.auction.buyer = self.bidder
        super().save(*args, **kwargs)

    
@receiver(post_save, sender=Bid)
def send_bid_update(sender, instance, **kwargs):
    
    if kwargs.get('created', False):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'auction_room',
            {
                'type': 'bid_message',
                'amount': float(instance.amount),
                'bidder': instance.bidder.username,
                'auction_id': instance.auction.id
            }
        )

# @receiver(pre_save, sender=Bid)
# def on_change(sender, instance, **kwargs):
#     old_bid = Bid.objects.filter(auction=instance.auction).order_by('-amount').first()
#     if old_bid and (float(instance.amount) <= float(old_bid.amount)):
#         raise Exception("Bid amount must be greater than the current highest bid amount")



