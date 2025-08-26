from django.contrib import admin
from .models import TravelOption, Booking

@admin.register(TravelOption)
class TravelOptionAdmin(admin.ModelAdmin):
    list_display = ('type', 'source', 'destination', 'date_time', 'price', 'available_seats')
    list_filter = ('type', 'date_time')
    search_fields = ('source', 'destination')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'user', 'travel_option', 'status', 'booking_date')
    list_filter = ('status', 'user')
    search_fields = ('user__username',)
