from django.urls import path

from .views import *

urlpatterns = [
    path('', home_page, name='manage_flight_home'),
    
    path('<int:flight_id>/', manage_flight, name='manage_flight'),
    
    path('add-flight/', add_flight, name='add_flight'),
    path('edit-flight/<int:flight_id>/', edit_flight, name='edit_flight'),
    path('delete-flight/<int:flight_id>/', delete_flight, name='delete_flight'),
    
    path('update-intermediate-airport/<int:flight_id>/', update_intermediate_airport, name='update_intermediate_airport'),
    
    path('add-ticket-class/<int:flight_id>/', add_flight_ticket_class, name='add_flight_ticket_class'),
    path('edit-ticket-class/<int:ticket_class_id>/', edit_flight_ticket_class, name='edit_flight_ticket_class'),
    path('delete-ticket-class/<int:ticket_class_id>/', delete_flight_ticket_class, name='delete_flight_ticket_class'),
]
