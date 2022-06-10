from django.urls import path

from base_app.decorators import employee_only

from .views import *

urlpatterns = [
    path('', index_page, name='manage_cost_home'),
    
    path('add-ticket-cost/', add_ticket_cost, name='add_ticket_cost'),
    path('edit-ticket-cost/<int:ticket_cost_id>/', edit_ticket_cost, name='edit_ticket_cost'),
    path('delete-ticket-cost/<int:ticket_cost_id>/', delete_ticket_cost, name='delete_ticket_cost'),
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