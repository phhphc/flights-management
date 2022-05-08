from django.forms import ModelForm, ValidationError
from django.utils import timezone

from .models import *


class CustomUserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'
        exclude = ['user']


class TicketCostForm(ModelForm):
    class Meta:
        model = TicketCost
        fields = '__all__'


class AirportForm(ModelForm):
    class Meta:
        model = Airport
        fields = '__all__'


class TicketClassForm(ModelForm):
    class Meta:
        model = TicketClass
        fields = '__all__'


class FlightForm(ModelForm):
    class Meta:
        model = Flight
        fields = '__all__'

    def clean(self):

        # check if flight time is bigger than minimum flight time
        flight_duration_min = Regulations.objects.get(pk=1).flight_duration_min
        if self.cleaned_data.get('duration') < flight_duration_min:
            raise ValidationError({
                'duration': 'Flight time is smaller than minimum flight time'})


class RegulationsForm(ModelForm):
    class Meta:
        model = Regulations
        fields = '__all__'


class NumberOfTicketForm(ModelForm):
    class Meta:
        model = NumberOfTicket
        fields = '__all__'
        exclude = ['flight']

    def __init__(self, flight_id, *args, **kwargs):
        self.flight_id = flight_id
        super(NumberOfTicketForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instant = super(NumberOfTicketForm, self).save(commit=False)

        # if instant.flight is None, add the flight
        if not self.instance.pk:
            instant.flight = Flight.objects.get(pk=self.flight_id)

        if commit:
            instant.save()
        return instant

    def clean(self):
        flight: Flight = Flight.objects.get(pk=self.flight_id)

        # check if the ticket class is duplicated
        if flight.numberofticket_set.filter(
                ticket_class=self.data['ticket_class']).exclude(pk=self.instance.pk):
            raise ValidationError({
                'ticket_class': ['Ticket class already exists for this flight'],
            })

        # check if the ticket cost is available
        if not TicketCost.objects.filter(
                ticket_class=self.data['ticket_class'],
                arrival_airport=flight.arrival_airport,
                departure_airport=flight.departure_airport).exists():
            raise ValidationError({
                'ticket_class': [f'Ticket cost is not available for this ticket class from {flight.departure_airport} to {flight.arrival_airport}'],
            })

        # check if quantity of ticket is bigger than customer's tickets
        customer_tickets_count = flight.ticket_set.filter(
            ticket_class=self.data['ticket_class']).count()
        if int(self.data['quantity']) < customer_tickets_count:
            raise ValidationError({
                'quantity': [f'There are {customer_tickets_count} customer\'s tickets of this ticket class'],
            })


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['flight', 'ticket_class', 'customer_name',
                  'customer_id_card', 'customer_phone']

    def __init__(self, user=None, employee=None, edit=False, *args, **kwargs):
        self.user = user
        self.employee = employee
        self.edit = edit
        super(TicketForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instant = super(TicketForm, self).save(commit=False)

        if not self.instance.pk:  # if create new ticket
            # if user is not None, set the user
            if self.user:
                instant.user = self.user
            # if employee is not None, set the employee_paid and status to paid (2)
            if not self.edit and self.employee:
                instant.employee_paid = self.employee
                instant.status = 2
            # set cost to the ticket cost
            instant.set_cost()

        if commit:
            instant.save()
        return instant

    def clean(self):

        # TODO: check if the ticket class is existed

        # check if available ticket is enough
        total_ticket = NumberOfTicket.objects.get(
            flight__pk=self.data['flight'], ticket_class=self.data['ticket_class']).quantity
        exists_ticket_count = Ticket.objects.filter(
            flight=self.data['flight'], ticket_class=self.data['ticket_class']).count()
        if total_ticket <= exists_ticket_count:
            raise ValidationError({
                'ticket_class': [f'No tickets of this ticket class on this flight left !'],
            })

        # if new ticket is created not by employee (customer book)
        if not self.instance.pk and not self.employee:
            book_ticket_before_min = Regulations.objects.get(
                pk=1).book_ticket_before_min  # get the minimun booking time before flight
            # get the departure time of the flight
            departure_time = Flight.objects.get(
                pk=self.data['flight']).departure_time
            # can only book ticket before the departure time - book_ticket_before_min
            if departure_time - timezone.now() < book_ticket_before_min:
                raise ValidationError({
                    'flight': [f'You can only book ticket before {departure_time - book_ticket_before_min}'],
                })
