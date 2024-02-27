from django.db import models

# Create your models here.
class Payment(models.Model):
    acution = models.ForeignKey('auction.Auction', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    buyer = models.ForeignKey('users.User', on_delete=models.CASCADE)
    payment_date = models.DateTimeField()
    payment_method = models.CharField(max_length=20, choices=[('credit_card','credit_card'),('paypal','paypal')])
    status = models.CharField(max_length=20, default='pending', choices=[('pending','pending'),('completed','completed'),('failed','failed'),('refunded','refunded')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('auction', 'buyer')

    def __str__(self):
        return self.payer.name
    
    def save(self, *args, **kwargs):
        if self.status == 'completed':
            self.acution.status = 'completed'
            self.acution.save()
        super().save(*args, **kwargs)
    
    
    
