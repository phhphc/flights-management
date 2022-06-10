from django.urls import path

from base_app.decorators import employee_only

from .views import *

urlpatterns = [
    path('', home_page, name='manage_ticket_home'),
    
    path('add-ticket/', add_ticket, name='add_ticket'),
    path('edit-ticket/<int:ticket_id>/', edit_ticket, name='edit_ticket_employee'),
    path('delete-ticket/<int:ticket_id>/', delete_ticket, name='delete_ticket_employee'),
    path('pay-ticket/<int:ticket_id>/', pay_ticket, name='pay_ticket_employee'),
    path('export-ticket/<int:ticket_id>/', export_ticket, name='export_ticket_employee'),
]

# restrict whole app to employees only
def dec_patterns(patterns):
    decorated_patterns = []
    for pattern in patterns:
        callback = pattern.callback
        pattern.callback = employee_only(callback)
        pattern._callback = employee_only(callback)
        decorated_patterns.append(pattern)
    return decorated_patterns


url_patterns = dec_patterns(urlpatterns)