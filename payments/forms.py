from django import forms

class PaymentForm(forms.Form):
    card_id = forms.CharField(max_length=20)
    ccv = forms.CharField(max_length=3)
    expiration_date = forms.DateField()
    card_holder = forms.CharField(max_length=50)
    
    def clean(self):
        """
        Check payment data is valid
        """
        # TODO: check payment syntax is valid
        # if false raise forms.ValidationError ....
        
        # some more check here
        return super().clean()
    
    def save(self):
        """
        process payment
        throw error if payment is failed
        """
        pass

        