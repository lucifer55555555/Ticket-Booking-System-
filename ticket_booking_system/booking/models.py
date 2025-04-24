from django.db import models
from django.contrib.auth.models import User

class Show(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    available_seats = models.IntegerField()

    def __str__(self):
        return self.title

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    seats = models.IntegerField()
    booked_at = models.DateTimeField(auto_now_add=True)
