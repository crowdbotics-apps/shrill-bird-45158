from django.db import models

# Create your models here.

class Review(models.Model):
    comment = models.TextField()
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    vehicle = models.ForeignKey('vehicle.Vehicle', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.comment