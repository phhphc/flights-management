from django.urls import path

from .views import *

urlpatterns = [
    path('', report_dashboard, name='report_dashboard'),
]
