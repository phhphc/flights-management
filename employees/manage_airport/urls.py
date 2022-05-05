from django.urls import path

from .views import *

urlpatterns = [
    path('', index_page, name='manage_airport_home'),
    
    path('add-airport/', add_airport, name='add_airport'),
    path('edit-airport/<str:airport_id>/', edit_airport, name='edit_airport'),
    path('delete-airport/<str:airport_id>/', delete_airport, name='delete_airport'),
]
