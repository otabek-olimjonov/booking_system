from django.db import models
from django.contrib.auth.models import User

class ParkingSpot(models.Model):
    number = models.IntegerField(unique=True)
    status = models.CharField(max_length=10, choices=[('free', 'Free'), ('booked', 'Booked'), ('in_use', 'In Use')], default='free')
    door = models.BooleanField(default=False)  # True for open, False for closed
    booked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # New field

    def __str__(self):
        return f"Spot {self.number} - {self.status}"


class Payment(models.Model):
    amount = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # New field

    def __str__(self):
        return f"amount {self.amount} - {self.user.username if self.user else 'Unknown'}"