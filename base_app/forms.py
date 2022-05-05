from genericpath import exists
from django.forms import ModelForm, ValidationError

from .models import *


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


class IntermediateAirportForm(ModelForm):
    class Meta:
        model = IntermediateAirport
        fields = '__all__'
        exclude = ['flight']


class NumberOfTicketForm(ModelForm):
    class Meta:
        model = NumberOfTicket
        fields = '__all__'
        exclude = ['flight']

    def __init__(self, flight_id, *args, **kwargs):
        self.flight_id = flight_id
        super(NumberOfTicketForm, self).__init__(*args, **kwargs)

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
                dst_airport=flight.dst_airport,
                src_airport=flight.src_airport).exists():
            raise ValidationError({
                'ticket_class': [f'Ticket cost is not available for this ticket class from {flight.src_airport} to {flight.dst_airport}'],
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


    def clean(self):
        
        # TODO: check if the ticket class is existed
        
        # check if available ticket is enough
        total_ticket = NumberOfTicket.objects.get(flight__pk=self.data['flight'], ticket_class=self.data['ticket_class']).quantity
        exists_ticket_count = Ticket.objects.filter(flight=self.data['flight'], ticket_class=self.data['ticket_class']).count()
        if total_ticket <= exists_ticket_count:
            raise ValidationError({
                'ticket_class': [f'No tickets of this ticket class on this flight left !'],
            })
            
        # TODO: if new ticket is a booked ticket, check if time is `one` day earlier than the flight's departure time