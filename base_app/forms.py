from django.forms import ModelForm, ValidationError

from .models import *


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['flight', 'ticket_class', 'customer_name',
                  'customer_id_card', 'customer_phone']


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
