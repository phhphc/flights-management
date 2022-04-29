from attr import field
from django.forms import ModelForm
from models.models import Flight, NumberOfTicket, IntermediateAirport


class FlightForm(ModelForm):
    class Meta:
        model = Flight
        fields = '__all__'
        
        
class NumberOfTicketForm(ModelForm):
    class Meta:
        model = NumberOfTicket
        fields = '__all__'
        exclude = ['flight']
        
        
class IntermediateAirportForm(ModelForm):
    class Meta:
        model = IntermediateAirport
        fields = '__all__'
        exclude = ['flight']