from django.urls import path

from base_app.decorators import employee_only

from .views import *

urlpatterns = [
    path('', index_page, name='manage_airport_home'),
    
    path('add-airport/', add_airport, name='add_airport'),
    path('edit-airport/<str:airport_id>/', edit_airport, name='edit_airport'),
    path('delete-airport/<str:airport_id>/', delete_airport, name='delete_airport'),
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