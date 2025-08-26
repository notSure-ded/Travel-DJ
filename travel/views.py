from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import TravelOption, Booking
from .forms import UserProfileForm, BookingForm, TravelOptionFilterForm
from django.contrib import messages

def register(request):
    """ Handles user registration. """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('travel_options')
    else:
        form = UserCreationForm()
    return render(request, 'travel/register.html', {'form': form})

def user_login(request):
    """ Handles user login. """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('travel_options')
    else:
        form = AuthenticationForm()
    return render(request, 'travel/login.html', {'form': form})

@login_required
def user_logout(request):
    """ Handles user logout. """
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    """ Handles user profile updates. """
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'travel/profile.html', {'form': form})

def travel_options(request):
    """ Displays available travel options with filters. """
    options = TravelOption.objects.filter(available_seats__gt=0).order_by('date_time')
    form = TravelOptionFilterForm(request.GET)
    if form.is_valid():
        if form.cleaned_data.get('type'):
            options = options.filter(type=form.cleaned_data['type'])
        if form.cleaned_data.get('source'):
            options = options.filter(source__icontains=form.cleaned_data['source'])
        if form.cleaned_data.get('destination'):
            options = options.filter(destination__icontains=form.cleaned_data['destination'])
        if form.cleaned_data.get('date'):
            options = options.filter(date_time__date=form.cleaned_data['date'])
    return render(request, 'travel/travel_options.html', {'options': options, 'form': form})

@login_required
def book_travel(request, travel_id):
    """ Handles the booking of a travel option. """
    travel_option = get_object_or_404(TravelOption, travel_id=travel_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            seats = booking.number_of_seats
            if 0 < seats <= travel_option.available_seats:
                booking.user = request.user
                booking.travel_option = travel_option
                booking.total_price = travel_option.price * seats
                travel_option.available_seats -= seats
                travel_option.save()
                booking.save()
                messages.success(request, 'Booking successful!')
                return redirect('my_bookings')
            else:
                messages.error(request, 'Invalid number of seats or not enough seats available.')
    else:
        form = BookingForm()
    return render(request, 'travel/book_travel.html', {'form': form, 'travel_option': travel_option})

@login_required
def my_bookings(request):
    """ Displays the current user's bookings. """
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'travel/my_bookings.html', {'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    """ Handles the cancellation of a booking. """
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    if request.method == 'POST':
        booking.cancel()
        messages.success(request, 'Booking cancelled successfully.')
        return redirect('my_bookings')
    return render(request, 'travel/cancel_booking.html', {'booking': booking})
