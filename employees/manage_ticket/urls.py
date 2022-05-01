from django.urls import path

from .views import *

urlpatterns = [
    path('', home_page, name='manage_ticket_home'),

]
