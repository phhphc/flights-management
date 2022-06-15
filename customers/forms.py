from django import forms

from base_app.models import Ticket


class SeatForm(forms.Form):
    seat_position = forms.IntegerField(
        label='Seat Number',
        min_value=1,
        required=False)

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        super(SeatForm, self).__init__(*args, **kwargs)

        self.fields['seat_position'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Seat Number',
            'max': self.instance.flight_ticket.quantity,
        })

    def clean(self):

        flight_ticket = self.instance.flight_ticket
        total_ticket = flight_ticket.quantity

        # check if ticket status is not paid
        if self.instance.status > 1:
            raise forms.ValidationError('Ticket already paid')

        # check if ticket seat position is avalable
        seat_position = self.cleaned_data.get('seat_position')
        if seat_position is not None:
            if seat_position > total_ticket:
                raise forms.ValidationError({
                    'seat_position': [f'Seat position is not exists for this flight'],
                })
            if flight_ticket.ticket_set.filter(seat_position=seat_position).exists():
                raise forms.ValidationError({
                    'seat_position': [f'Seat position is unavailable'],
                })

    def save(self, commit=True):
        self.instance.seat_position = self.cleaned_data.get('seat_position')
        self.instance.status = 2
        if commit:
            self.instance.save()
        return self.instance


class CustomerTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['customer_name', 'customer_id_card',
                  'customer_phone', 'seat_position']

    # def __init__(self, *args, **kwargs):
    #     super(CustomerTicketForm, self).__init__(*args, **kwargs)
    #     if self.instance.status < 2:
    #         self.fields['seat_position'].widget.attrs.update({
    #             'class': 'hidden'
    #         })

    def clean(self):
        flight_ticket = self.instance.flight_ticket
        total_ticket = flight_ticket.quantity

        # check if ticket status is not confirm
        if self.instance.status > 2:
            raise forms.ValidationError(
                f'Cannot edit ticket in {self.instance.str_status} status')

        # check if ticket seat position is avalable
        seat_position = self.cleaned_data.get('seat_position')
        if seat_position is not None:
            if seat_position > total_ticket:
                raise forms.ValidationError({
                    'seat_position': [f'Seat position is not exists for this flight'],
                })
            if flight_ticket.ticket_set.filter(seat_position=seat_position).exists():
                raise forms.ValidationError({
                    'seat_position': [f'Seat position is unavailable'],
                })

    def save(self, commit=True):
        obj = super(CustomerTicketForm, self).save(commit=False)
        # if self.instance.status < 2:
        #     obj.seat_position = None
        if commit:
            obj.save()
        return obj
