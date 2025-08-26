from django.db import models
from django.contrib.auth.models import User

class TravelOption(models.Model):
    """
    Represents a travel option (Flight, Train, Bus).
    This model stores all details about a specific journey.
    """
    TRAVEL_TYPES = (
        ('Flight', 'Flight'),
        ('Train', 'Train'),
        ('Bus', 'Bus'),
    )

    travel_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=10, choices=TRAVEL_TYPES)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_seats = models.PositiveIntegerField()

    def __str__(self):
        # FIX: Removed the date and time to match the test expectation.
        return f"{self.type} from {self.source} to {self.destination}"

class Booking(models.Model):
    """
    Represents a user's booking for a TravelOption.
    This model links a user to a travel option and stores booking details.
    """
    BOOKING_STATUS = (
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    )

    booking_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    travel_option = models.ForeignKey(TravelOption, on_delete=models.CASCADE)
    number_of_seats = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=BOOKING_STATUS, default='Confirmed')

    def __str__(self):
        return f"Booking {self.booking_id} by {self.user.username}"

    def cancel(self):
        """
        Marks the booking as cancelled and returns the booked seats to the travel option.
        """
        if self.status == 'Confirmed':
            self.status = 'Cancelled'
            self.travel_option.available_seats += self.number_of_seats
            self.travel_option.save()
            self.save()
