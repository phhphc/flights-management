import django_filters

from .models import *


class TicketCostFilter(django_filters.FilterSet):
    class Meta:
        model = TicketCost
        fields = {
            'departure_airport': ['exact'],
            'arrival_airport': ['exact'],
            'ticket_class': ['exact'],
            'cost': ['gte', 'lte'],
        }


class FlightFilter(django_filters.FilterSet):
    class Meta:
        model = Flight
        fields = {
            'departure_airport': ['exact'],
            'arrival_airport': ['exact'],
            'departure_time': ['date__exact', 'date__gte', 'date__lte'],
        }
