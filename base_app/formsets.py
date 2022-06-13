from django.forms import BaseInlineFormSet, ValidationError
from django.db.models import Max

from .models import *


class BaseIntermediateAirportFormSet(BaseInlineFormSet):

    def clean(self):
        if any(self.errors):
            return

        regulations = Regulations.objects.get(pk=1)
        intermediate_airport_time_min = regulations.intermediate_airport_time_min
        intermediate_airport_time_max = regulations.intermediate_airport_time_max
        airports = []

        for form in self.forms:
            # ignore deleted forms
            if self.can_delete and self._should_delete_form(form):
                continue
            # ignore empty forms
            if form.empty_permitted:
                continue

            # check that no intermediate airport is duplicated
            airport = form.cleaned_data.get('airport')
            if airport in airports:
                form.add_error(
                    'airport', ['Intermediate airport is duplicated'])
            airports.append(airport)

            # check if stop time is bigger than intermediate_airport_time_min
            # check if stop time is smaller than intermediate_airport_time_max
            stop_time = form.cleaned_data.get('stop_time')
            if stop_time < intermediate_airport_time_min:
                form.add_error(
                    'stop_time', ['Stop time is smaller than minimum'])
            if stop_time > intermediate_airport_time_max:
                form.add_error(
                    'stop_time', ['Stop time is bigger than maximum'])


class BaseFlightTicketsFormSet(BaseInlineFormSet):

    def clean(self):
        if any(self.errors):
            return

        ticket_class_list = []
        for form in self.forms:
            # ignore empty forms
            if form.empty_permitted:
                continue

            ticket_class = form.cleaned_data.get('ticket_class')
            try:
                # if form is delete
                # If there are any tickets for this class, prevent delete and send error message
                if self.can_delete and self._should_delete_form(form):
                    if self.instance.flightticket_set.get(ticket_class=ticket_class).ticket_set.exists():
                        raise ValidationError(
                            f'Cannot delete ticket class {ticket_class} because there are tickets for this class')
                    continue

                # check that no ticket_class is duplicated
                if ticket_class.pk in ticket_class_list:
                    form.add_error(
                        'ticket_class', ['Ticket_class is duplicated'])
                ticket_class_list.append(ticket_class.pk)

                # check if ticket cost is available
                if not TicketCost.objects.filter(
                        departure_airport=self.instance.departure_airport,
                        arrival_airport=self.instance.arrival_airport,
                        ticket_class=ticket_class).exists():
                    form.add_error(
                        'ticket_class', [
                            f'There are no price for this ticket class form {self.instance.departure_airport} to {self.instance.arrival_airport}'])

                # check if quantity of ticket is bigger than customer's tickets
                tickets = self.instance.flightticket_set.get(
                    ticket_class=ticket_class).ticket_set
                customer_tickets_count = tickets.count()
                if form.cleaned_data.get('quantity') < customer_tickets_count:
                    form.add_error(
                        'quantity', [
                            f'There are {customer_tickets_count} customer\'s tickets of this ticket class'])
                    
                # check if quantity of ticket is bigger or equal to max seat_position
                max_seat_position = tickets.aggregate(Max('seat_position'))['seat_position__max']
                if max_seat_position is not None:
                    if form.cleaned_data.get('quantity') < max_seat_position:
                        form.add_error(
                            'quantity', [
                                f'There are seat_position {max_seat_position} of this ticket class on this flight'])
                
            except FlightTicket.DoesNotExist:
                pass

    def save(self, commit=True):
        obj_list = super(BaseFlightTicketsFormSet, self).save(commit=False)
        for obj in obj_list:
            if not obj.cost:
                obj.set_cost()
            if commit:
                obj.save()

        for obj in self.deleted_objects:
            obj.delete()

        return obj_list
