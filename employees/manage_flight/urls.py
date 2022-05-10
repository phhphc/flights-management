from django.urls import path

from .views import *

urlpatterns = [
    path('', home_page, name='manage_flight_home'),
    
    path('<int:flight_id>/', manage_flight, name='manage_flight'),
    
    path('add-flight/', add_flight, name='add_flight'),
    path('edit-flight/<int:flight_id>/', edit_flight, name='edit_flight'),
    path('delete-flight/<int:flight_id>/', delete_flight, name='delete_flight'),
    
    path('update-intermediate-airport/<int:flight_id>/', update_intermediate_airport, name='update_intermediate_airport'),
    path('update-ticket-class/<int:flight_id>/', update_flight_ticket_class, name='update_flight_ticket_class'),
]
