from django.forms import BaseInlineFormSet

from .models import *


class BaseIntermediateAirportFormSet(BaseInlineFormSet):

    def clean(self):
        # Don't bother validating the formset unless each form is valid on its own
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
