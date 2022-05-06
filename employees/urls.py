from django.urls import path, include

from .views import *

# TODO: restrict access to this url to employees only
urlpatterns = [
    path('', home_page, name='employee_home'),
    path('manage-airport/', include('employees.manage_airport.urls')),
    path('manage-cost/', include('employees.manage_cost.urls')),
    path('manage-ticket-class/', include('employees.manage_ticket_class.urls')),
    path('manage-flight/', include('employees.manage_flight.urls')),
    path('manage-ticket/', include('employees.manage_ticket.urls')),
    path('manage-regulations/', include('employees.manage_regulations.urls')),
    path('view-report/', include('employees.view_report.urls')),
]
