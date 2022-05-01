from django.urls import path, include

from .views import *

urlpatterns = [
    path('', home_page, name='employee_home'),
    path('manage-flight/', include('employees.manage_flight.urls')),
    path('manage-ticket/', include('employees.manage_ticket.urls')),
    path('view-report/', include('employees.view_report.urls')),

]
