from django.db import models
from django.contrib.auth.models import User
import string
import random

class Airport(models.Model):
    code = models.CharField(max_length=3, unique=True)
    city = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.city} ({self.code})"

class Flight(models.Model):
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    duration = models.IntegerField()
    capacity = models.IntegerField(default = 50) # type: ignore

    def __str__(self):
        return f"{self.origin} to {self.destination} - {self.duration} min"


# наследуем тут Юзера, чтобы расширить его функционал (просто фановое расширение)
class Passenger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE , blank=True, null=True , related_name='passenger_profile')
    passport_number = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} — {self.passport_number}"



class Booking(models.Model):
    passenger = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="bookings")
    booking_code = models.CharField(max_length=64, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.booking_code:
            self.booking_code = self.generate_booking_code()
        super().save(*args, **kwargs)

    def generate_booking_code(self):
        letters = string.ascii_uppercase
        numbers = string.digits
        return ''.join(random.choices(letters + numbers, k=10))

    def __str__(self):
        return f"Booking: {self.booking_code} — {self.passenger} на рейс {self.flight}"