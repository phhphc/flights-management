from django.urls import path

from .views import *

urlpatterns = [
    path('', index_page, name='manage_ticket_class_home'),
    
    path('add-ticket-class/', add_ticket_class, name='add_ticket_class'),
    path('edit-ticket-class/<int:ticket_class_id>/', edit_ticket_class, name='edit_ticket_class'),
    path('delete-ticket-class/<int:ticket_class_id>/', delete_ticket_class, name='delete_ticket_class'),
]
