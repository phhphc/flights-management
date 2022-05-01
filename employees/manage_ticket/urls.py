from django.urls import path

from .views import *

urlpatterns = [
    path('', home_page, name='manage_ticket_home'),
    
    path('add-ticket/', add_ticket, name='add_ticket'),
    path('edit-ticket/<int:ticket_id>/', edit_ticket, name='edit_ticket_employee'),
    path('delete-ticket/<int:ticket_id>/', delete_ticket, name='delete_ticket_employee'),
    path('pay-ticket/<int:ticket_id>/', pay_ticket, name='pay_ticket_employee'),
    path('export-ticket/<int:ticket_id>/', export_ticket, name='export_ticket_employee'),
]
