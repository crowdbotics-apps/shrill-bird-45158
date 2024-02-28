from django.db import models


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
    buyer = models.ForeignKey('users.User', related_name='buyer', on_delete=models.CASCADE)
    seller = models.ForeignKey('users.User', related_name='seller', on_delete=models.CASCADE)
    vehicle = models.OneToOneField('vehicle.Vehicle', on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=auction_status_choices, default='open')
    auctioned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('vehicle', 'buyer')


    def __str__(self):
        return self.vehicle.name
    

class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    buyer = models.ForeignKey('users.User', on_delete=models.CASCADE)
    won = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
        
    def save(self, *args, **kwargs):
        if self.won:
            if self.amount > self.auction.highest_bid:
                self.auction.highest_bid = self.amount
                self.auction.buyer = self.buyer
        super().save(*args, **kwargs)

    def __str__(self):
        return self.auction.vehicle.name