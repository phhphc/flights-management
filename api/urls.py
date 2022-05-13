from django.urls import path

from .views import *


urlpatterns = [
    path('flight-seats/<int:flight_id>/<int:ticket_class_id>', flight_seat_list, name='api_flight_seat_list'), 
]
