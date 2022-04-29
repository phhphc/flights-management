from django.urls import path

from .views import *

urlpatterns = [
    path('', home_page, name='employee_home'),
    
    path('manage-flight/<int:flight_id>/', manage_flight, name='manage_flight'),
    
    path('add-flight/', add_flight, name='add_flight'),
    path('edit-flight/<int:flight_id>/', edit_flight, name='edit_flight'),
    path('delete-flight/<int:flight_id>/', delete_flight, name='delete_flight'),
    
    path('add-intermediate-airport/<int:flight_id>/', add_intermediate_airport, name='add_intermediate_airport'),
    path('edit-intermediate-airport/<int:intermediate_airport_id>/', edit_intermediate_airport, name='edit_intermediate_airport'),
    path('delete-intermediate-airport/<int:intermediate_airport_id>/', delete_intermediate_airport, name='delete_intermediate_airport'),
    
    path('add-ticket/<int:flight_id>/', add_ticket, name='add_ticket'),
    path('edit-ticket/<int:ticket_id>/', edit_ticket, name='edit_ticket'),
    path('delete-ticket/<int:ticket_id>/', delete_ticket, name='delete_ticket'),
]
