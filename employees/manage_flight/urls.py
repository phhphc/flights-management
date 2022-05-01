from django.urls import path

from .views import *

urlpatterns = [
    path('', home_page, name='manage_flight_home'),
    
    path('<int:flight_id>/', manage_flight, name='manage_flight'),
    
    path('add-flight/', add_flight, name='add_flight'),
    path('edit-flight/<int:flight_id>/', edit_flight, name='edit_flight'),
    path('delete-flight/<int:flight_id>/', delete_flight, name='delete_flight'),
    
    path('add-intermediate-airport/<int:flight_id>/', add_intermediate_airport, name='add_intermediate_airport'),
    path('edit-intermediate-airport/<int:intermediate_airport_id>/', edit_intermediate_airport, name='edit_intermediate_airport'),
    path('delete-intermediate-airport/<int:intermediate_airport_id>/', delete_intermediate_airport, name='delete_intermediate_airport'),
    
    path('add-ticket-class/<int:flight_id>/', add_ticket_class, name='add_ticket_class'),
    path('edit-ticket-class/<int:ticket_class_id>/', edit_ticket_class, name='edit_ticket_class'),
    path('delete-ticket-class/<int:ticket_class_id>/', delete_ticket_class, name='delete_ticket_class'),
]
