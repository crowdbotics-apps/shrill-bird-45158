from django.db import models

# Create your models here.

class Review(models.Model):
    comment = models.TextField()
    buyer = models.ForeignKey('buyer.Buyer', on_delete=models.CASCADE)

    def __str__(self):  # __unicode__ on Python 2
        return self.comment