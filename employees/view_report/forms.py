from secrets import choice
from django import forms
from datetime import date


class MonthYearForm(forms.Form):
    month = forms.ChoiceField(choices=[(m, m) for m in range(1, 13)])
    year = forms.ChoiceField(choices=[(y, y)
                             for y in range(2015, date.today().year+1)])
