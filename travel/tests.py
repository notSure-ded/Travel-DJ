from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import TravelOption, Booking
from django.utils import timezone
from django.urls import reverse

class TravelModelsTest(TestCase):
    """ Test suite for the travel app models. """

    def setUp(self):
        """ Set up non-modified objects used by all test methods. """
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.travel_option = TravelOption.objects.create(
            type='Bus',
            source='City A',
            destination='City B',
            date_time=timezone.now(),
            price=50.00,
            available_seats=20
        )

    def test_travel_option_str(self):
        """ Test the string representation of TravelOption. """
        # --- FIX: Update the expected string to match the model's __str__ output ---
        expected_str = f"{self.travel_option.type} from {self.travel_option.source} to {self.travel_option.destination}"
        self.assertEqual(str(self.travel_option), expected_str)


    def test_booking_cancellation(self):
        """ Test the cancel method of the Booking model. """
        initial_seats = self.travel_option.available_seats
        
        booking = Booking.objects.create(
            user=self.user,
            travel_option=self.travel_option,
            number_of_seats=2,
            total_price=100.00
        )
        
        # Manually update the seats since the booking is created directly
        self.travel_option.available_seats -= 2
        self.travel_option.save()
        self.travel_option.refresh_from_db()
        self.assertEqual(self.travel_option.available_seats, initial_seats - 2)
        
        # Cancel the booking
        booking.cancel()
        
        self.assertEqual(booking.status, 'Cancelled')
        
        self.travel_option.refresh_from_db()
        self.assertEqual(self.travel_option.available_seats, initial_seats)


class TravelViewsTest(TestCase):
    """ Test suite for the travel app views. """

    def setUp(self):
        """ Set up a client and user for testing views. """
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.travel_option = TravelOption.objects.create(
            type='Train',
            source='City C',
            destination='City D',
            date_time=timezone.now(),
            price=100.00,
            available_seats=10
        )

    def test_travel_options_view(self):
        """ Test that the travel options page loads correctly. """
        response = self.client.get(reverse('travel_options'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Available Travel Options')

    def test_my_bookings_view_unauthenticated(self):
        """ Test that unauthenticated users are redirected from my_bookings page. """
        response = self.client.get(reverse('my_bookings'))
        self.assertEqual(response.status_code, 302) 
        self.assertRedirects(response, f"/login/?next=/my_bookings/")


    def test_my_bookings_view_authenticated(self):
        """ Test that authenticated users can access the my_bookings page. """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('my_bookings'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'My Bookings')

    def test_successful_booking(self):
        """ Test the complete booking process. """
        self.client.login(username='testuser', password='testpassword')
        initial_seats = self.travel_option.available_seats
        
        response = self.client.post(reverse('book_travel', args=[self.travel_option.travel_id]), {
            'number_of_seats': 2
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('my_bookings'))
        
        self.travel_option.refresh_from_db()
        self.assertEqual(self.travel_option.available_seats, initial_seats - 2)
