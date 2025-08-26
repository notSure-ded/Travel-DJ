from django import forms
from django.contrib.auth.models import User
from .models import Booking, TravelOption

class UserProfileForm(forms.ModelForm):
    """
    Form for updating user profile information (first name, last name, email).
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class BookingForm(forms.ModelForm):
    """
    Form for creating a new booking, allowing user to specify the number of seats.
    """
    class Meta:
        model = Booking
        fields = ('number_of_seats',)
        labels = {
            'number_of_seats': 'Number of Seats',
        }

class TravelOptionFilterForm(forms.Form):
    """
    Form for filtering available travel options based on type, source, destination, and date.
    """
    # Dynamically create choices for the travel type filter, including an 'All' option
    TRAVEL_TYPE_CHOICES = [('', 'All Types')] + list(TravelOption.TRAVEL_TYPES)
    
    type = forms.ChoiceField(choices=TRAVEL_TYPE_CHOICES, required=False, label="Type")
    source = forms.CharField(max_length=100, required=False, label="Source")
    destination = forms.CharField(max_length=100, required=False, label="Destination")
    date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Date")
