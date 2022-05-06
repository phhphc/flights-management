from django.urls import path

from .views import *

urlpatterns = [
    path('', index_page, name='manage_regulations_home'),
    
    path('edit-regulations/', edit_regulations, name='edit_regulations'),
]
