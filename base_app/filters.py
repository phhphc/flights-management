import django_filters
from django import forms

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
            'departure_airport__city': ['exact'],
            'departure_airport': ['exact'],
            'arrival_airport__city': ['exact'],
            'arrival_airport': ['exact'],
            'departure_time': ['date__exact', 'date__gte', 'date__lte'],
        }

    def __init__(self, *args, **kwargs):
        super(FlightFilter, self).__init__(*args, **kwargs)

        self.form.fields['departure_time__date__lte'].widget = forms.widgets.DateInput(
            attrs={'type': 'date'})
        self.form.fields['departure_time__date__gte'].widget = forms.widgets.DateInput(
            attrs={'type': 'date'})


class TicketFilter(django_filters.FilterSet):
    class Meta:
        model = Ticket
        fields = {
            'flight_ticket__flight__departure_airport': ['exact'],
            'flight_ticket__flight__departure_airport__city': ['exact'],
            'flight_ticket__flight__arrival_airport': ['exact'],
            'flight_ticket__flight__arrival_airport__city': ['exact'],
            'flight_ticket__flight__departure_time': ['date__gte', 'date__lte'],
            'flight_ticket__ticket_class': ['exact'],
            'status': ['exact'],
        }

    def __init__(self, *args, **kwargs):
        super(TicketFilter, self).__init__(*args, **kwargs)

        self.form.fields['flight_ticket__flight__departure_time__date__lte'].widget = forms.widgets.DateInput(
            attrs={'type': 'date'})
        self.form.fields['flight_ticket__flight__departure_time__date__gte'].widget = forms.widgets.DateInput(
            attrs={'type': 'date'})
