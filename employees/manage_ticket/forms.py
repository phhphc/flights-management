from django.forms import ModelForm
from models.models import Ticket


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'
        exclude = ['user', 'status', 'employee_paid', 'cost']
