from django.urls import path

from base_app.decorators import employee_only

from .views import *

urlpatterns = [
    path('', index_page, name='manage_ticket_class_home'),
    
    path('add-ticket-class/', add_ticket_class, name='add_ticket_class'),
    path('edit-ticket-class/<int:ticket_class_id>/', edit_ticket_class, name='edit_ticket_class'),
    path('delete-ticket-class/<int:ticket_class_id>/', delete_ticket_class, name='delete_ticket_class'),
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