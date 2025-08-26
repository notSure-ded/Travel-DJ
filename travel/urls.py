from django.urls import path
from . import views

urlpatterns = [
    # User management URLs
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),

    # Travel and booking URLs
    path('', views.travel_options, name='travel_options'),
    path('book/<int:travel_id>/', views.book_travel, name='book_travel'),
    path('my_bookings/', views.my_bookings, name='my_bookings'),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]
