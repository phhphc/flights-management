from attr import field
from base_app.forms import TicketForm


class EmployeeTicketsForm(TicketForm):
   class Meta:
       model = TicketForm.Meta.model
       fields = TicketForm.Meta.fields + ['seat_position']