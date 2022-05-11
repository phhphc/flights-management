from django.urls import path

from .views import *


urlpatterns = [
    path('', home_page, name='home'),
    
    path('profile/', profile_page, name='profile'),
    
    path('flight/<int:flight_id>', flight_detail, name='flight_detail'),
    path('book-flight/', book_flight, name='book_flight'),   
    path('book-flight-confirm/<int:ticket_id>', book_flight_confirm, name='book_flight_confirm'),  
    path('edit-ticket/<int:ticket_id>', edit_ticket_customer, name='edit_ticket_customer'), 
    path('delete-book-flight/<int:ticket_id>', delete_book_flight, name='delete_book_flight'),   
]
