from django.contrib import messages
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory

from base_app.models import TicketClass, Flight, IntermediateAirport, FlightTicket, Regulations
from base_app.forms import FlightForm
from base_app.formsets import BaseIntermediateAirportFormSet, BaseFlightTicketsFormSet
from base_app.filters import FlightFilter


def home_page(request):
    flights = Flight.objects.all().order_by('-pk')
    flight_filter = FlightFilter(request.GET, queryset=flights)
    flights = flight_filter.qs

    return render(request, 'employees/manage_flight/index.html', {
        'flights': flights,
        "flight_filter": flight_filter,
    })


def manage_flight(request, flight_id):
    flight = Flight.objects.get(pk=flight_id)
    intermediate_airports = IntermediateAirport.objects.filter(
        flight=flight)
    flight_tickets = FlightTicket.objects.filter(flight__pk=flight_id)

    return render(request, 'employees/manage_flight/manage_flight.html', {
        'flight': flight,
        'intermediate_airports': intermediate_airports,
        'flight_tickets': flight_tickets,
    })


def add_flight(request):
    form = FlightForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            obj = form.save()
            return redirect('manage_flight', flight_id=obj.pk)

    return render(request, 'employees/manage_flight/add_flight.html', {
        'form': form,
    })


def edit_flight(request, flight_id):
    flight = Flight.objects.get(pk=flight_id)
    form = FlightForm(request.POST or None, instance=flight)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('manage_flight', flight_id=flight_id)

    return render(request, 'employees/manage_flight/edit_flight.html', {
        'form': form,
        'flight_id': flight_id,
    })


def delete_flight(request, flight_id):
    flight = Flight.objects.get(pk=flight_id)
    flight.delete()

    return redirect('employee_home')


def update_intermediate_airport(request, flight_id):
    intermediate_airport_max = Regulations.objects.get(
        pk=1).intermediate_airport_max

    IntermediateAirportFormSet = inlineformset_factory(
        Flight, IntermediateAirport,
        fields=['airport', 'stop_time', 'notes'],
        formset=BaseIntermediateAirportFormSet,
        max_num=intermediate_airport_max,
        validate_max=True)

    flight = Flight.objects.get(pk=flight_id)
    formset = IntermediateAirportFormSet(request.POST or None, instance=flight)

    if request.method == 'POST':
        if formset.is_valid():
            formset.save()
            return redirect('manage_flight', flight_id=flight_id)

    return render(request, 'employees/manage_flight/update_intermediate_aitport.html', {
        'formset': formset,
        'flight_id': flight_id,
    })


def update_flight_ticket_class(request, flight_id):
    
    FlightTicketFormSet = inlineformset_factory(
        Flight, FlightTicket,
        fields=['ticket_class', 'quantity'],
        formset=BaseFlightTicketsFormSet,
        max_num = TicketClass.objects.all().count(),
        validate_max=True)
    
    flight = Flight.objects.get(pk=flight_id)
    formset = FlightTicketFormSet(request.POST or None, instance=flight)
    
    if request.method == 'POST':
        if formset.is_valid():
            formset.save()
            return redirect('manage_flight', flight_id=flight_id)

    return render(request, 'employees/manage_flight/update_flight_ticket_class.html', {
        'formset': formset,
        'flight_id': flight_id,
    })
