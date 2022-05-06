from django.contrib import messages
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory

from base_app.models import Ticket, Flight, IntermediateAirport, NumberOfTicket, Regulations
from base_app.forms import FlightForm, NumberOfTicketForm
from base_app.formsets import BaseIntermediateAirportFormSet


def home_page(request):
    flights = Flight.objects.all().order_by('-pk')

    return render(request, 'employees/manage_flight/index.html', {
        'flights': flights,
    })


def manage_flight(request, flight_id):
    flight = Flight.objects.get(pk=flight_id)
    intermediate_airports = IntermediateAirport.objects.filter(
        flight=flight)
    tickets = NumberOfTicket.objects.filter(flight__pk=flight_id)

    return render(request, 'employees/manage_flight/manage_flight.html', {
        'flight': flight,
        'intermediate_airports': intermediate_airports,
        'tickets': tickets,
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


def add_flight_ticket_class(request, flight_id):
    form = NumberOfTicketForm(flight_id=flight_id, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('manage_flight', flight_id=flight_id)

    return render(request, 'employees/manage_flight/add_flight_ticket_class.html', {
        'form': form,
        'flight_id': flight_id,
    })


def edit_flight_ticket_class(request, ticket_class_id):
    ticket = NumberOfTicket.objects.get(pk=ticket_class_id)
    form = NumberOfTicketForm(
        flight_id=ticket.flight.pk, data=request.POST or None, instance=ticket)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('manage_flight', flight_id=ticket.flight.pk)

    return render(request, 'employees/manage_flight/edit_flight_ticket_class.html', {
        'form': form,
        'flight_id': ticket.flight.pk,
    })


def delete_flight_ticket_class(request, ticket_class_id):
    ticket = NumberOfTicket.objects.get(pk=ticket_class_id)

    # If there are any tickets for this class, do not delete and send error message
    if Ticket.objects.filter(
            ticket_class=ticket.ticket_class.id, flight=ticket.flight.pk).exists():
        messages.error(
            request, 'Cannot delete ticket class. There are customer tickets for this class.')
        print('hi')
    else:
        ticket.delete()

    return redirect('manage_flight', flight_id=ticket.flight.pk)
