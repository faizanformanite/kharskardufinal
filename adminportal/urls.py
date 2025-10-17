from django.urls import path, include
from django.contrib import admin
from . import views
urlpatterns = [
    path('', views.home, name='admin-home'),
    path('rooms/', views.rooms, name='admin-rooms'),
    path('gallery/', views.gallery, name='admin-gallery'),
    path('check-availability/', views.checkAvailability, name='check-Availability'),
    path('book-room/', views.book, name='admin-bookings')
    # add_booking_admin_room_wise
    ,path('add-booking-admin-room-wise/', views.add_booking_admin_room_wise, name='add_booking_admin_room_wise'),
    # checkin
    path('checkin/<int:id>/', views.checkin, name='checkin'),
    # checkout
    path('checkout/<int:id>/', views.checkout, name='checkout'),
    # download ticket
    path('download-ticket/<int:id>/', views.download_ticket, name='download_ticket'),
    path('admin/booking/success/', views.admin_booking_success, name='admin_booking_success'),


]