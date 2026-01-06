from django.db import models
from django.contrib.auth.models import User
from turf.models import Turf
import uuid

class TurfBooking(models.Model):

    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    turf = models.ForeignKey(Turf, on_delete=models.CASCADE, related_name='booking_requests')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    booking_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    total_hours = models.PositiveIntegerField()
    base_amount = models.PositiveIntegerField()
    light_charge = models.PositiveIntegerField()
    total_amount = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.turf.turf_name} | {self.booking_date}"
