from django.forms import ModelForm
from models.models import Ticket


class BookTicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'
        exclude = ['status', 'user', 'employee_paid']