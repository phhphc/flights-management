from django.urls import path

from .views import *


urlpatterns = [
    path('', home_page, name='home'),
    path('flight/<int:flight_id>', flight_detail, name='flight_detail'),
    path('book-flight/', book_flight, name='book_flight'),   
]
