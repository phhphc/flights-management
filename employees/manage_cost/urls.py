from django.urls import path

from .views import *

urlpatterns = [
    path('', index_page, name='manage_cost_home'),
    
    path('add-ticket-cost/', add_ticket_cost, name='add_ticket_cost'),
    path('edit-ticket-cost/<int:ticket_cost_id>/', edit_ticket_cost, name='edit_ticket_cost'),
    path('delete-ticket-cost/<int:ticket_cost_id>/', delete_ticket_cost, name='delete_ticket_cost'),
]
