from django.forms import ModelForm, ValidationError
from django import forms
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
        
        
    def __init__(self, *args, **kwargs):
        super(FlightForm, self).__init__(*args, **kwargs)

        print(self.fields)
        self.fields['departure_time'].widget = forms.widgets.DateInput(
            attrs={'type': 'date'})

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


class TicketForm(ModelForm):
    flight = forms.ModelChoiceField(queryset=Flight.objects.all())
    ticket_class = forms.ModelChoiceField(queryset=TicketClass.objects.all())

    class Meta:
        model = Ticket
        fields = ['customer_name',
                  'customer_id_card', 'customer_phone', 'seat_position']

    def __init__(self, user=None, employee=None, edit=False, *args, **kwargs):
        self.user = user
        self.employee = employee
        self.edit = edit

        super(TicketForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['flight'].initial = self.instance.flight_ticket.flight.pk
            self.fields['ticket_class'].initial = self.instance.flight_ticket.ticket_class.pk

    def save(self, commit=True):
        instant = super(TicketForm, self).save(commit=False)

        if not self.instance.pk:  # if create new ticket
            # if user is not None, set the user
            if self.user.is_authenticated:
                instant.user = self.user
            # if employee is not None, set the employee_paid and status to paid (2)
            if not self.edit and self.employee:
                instant.employee_paid = self.employee
                instant.status = 2
            # set flight_ticket

        instant.flight_ticket = FlightTicket.objects.get(
            flight__pk=self.data['flight'], ticket_class__pk=self.data['ticket_class'])

        if commit:
            instant.save()
        return instant

    def clean(self):

        # check if ticket_type is avalable
        try:
            flight_ticket = FlightTicket.objects.get(
                flight__pk=self.data['flight'], ticket_class=self.data['ticket_class'])
            total_ticket = flight_ticket.quantity
        except FlightTicket.DoesNotExist:
            raise ValidationError({
                'ticket_class': [f'Ticket class is not available for this flight'],
            })
        exists_ticket_count = Ticket.objects.filter(
            flight_ticket__flight=self.data['flight'], flight_ticket__ticket_class=self.data['ticket_class']).count()
        if total_ticket <= exists_ticket_count:
            raise ValidationError({
                'ticket_class': [f'No tickets of this ticket class on this flight left !'],
            })

        # check if ticket seat position is avalable
        seat_position = self.cleaned_data.get('seat_position')
        if seat_position is not None:
            if seat_position > total_ticket:
                raise ValidationError({
                    'seat_position': [f'Seat position is not exists for this flight'],
                })
            if flight_ticket.ticket_set.filter(seat_position=seat_position).exists():
                raise ValidationError({
                    'seat_position': [f'Seat position is unavailable'],
                })

        # if new ticket is created not by employee (customer book)
        # check if time before the departure time - book_ticket_before_min
        if not self.instance.pk and not self.employee:
            book_ticket_before_min = Regulations.objects.get(
                pk=1).book_ticket_before_min  # get the minimun booking time before flight
            # get the departure time of the flight
            departure_time = Flight.objects.get(
                pk=self.data['flight']).departure_time
            # check time
            if departure_time - timezone.now() < book_ticket_before_min:
                raise ValidationError({
                    'flight': [f'You can only book ticket before {departure_time - book_ticket_before_min}'],
                })
