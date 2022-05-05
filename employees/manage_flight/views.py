from django.contrib import messages
from django.shortcuts import render, redirect

from base_app.models import Ticket, Flight, IntermediateAirport, NumberOfTicket
from base_app.forms import FlightForm, IntermediateAirportForm, NumberOfTicketForm


def home_page(request):
    flights = Flight.objects.all().order_by('-pk')

    return render(request, 'employees/manage_flight/index.html', {
        'flights': flights,
    })


def manage_flight(request, flight_id):
    flight = Flight.objects.get(pk=flight_id)
    intermediate_airports = IntermediateAirport.objects.filter(
        flight=flight).order_by('sequence')
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


def add_intermediate_airport(request, flight_id):
    form = IntermediateAirportForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            obj.flight = Flight.objects.get(pk=flight_id)
            obj.save()
            return redirect('manage_flight', flight_id=flight_id)

    return render(request, 'employees/manage_flight/add_intermediate_aitport.html', {
        'form': form,
        'flight_id': flight_id,
    })


def edit_intermediate_airport(request, intermediate_airport_id):
    airport = IntermediateAirport.objects.get(pk=intermediate_airport_id)
    form = IntermediateAirportForm(request.POST or None, instance=airport)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('manage_flight', flight_id=airport.flight.pk)

    return render(request, 'employees/manage_flight/edit_intermediate_airport.html', {
        'form': form,
        'flight_id': airport.flight.pk,
    })


def delete_intermediate_airport(request, intermediate_airport_id):
    airport = IntermediateAirport.objects.get(pk=intermediate_airport_id)
    airport.delete()

    return redirect('manage_flight', flight_id=airport.flight.pk)


def add_flight_ticket_class(request, flight_id):
    form = NumberOfTicketForm(flight_id=flight_id, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            obj.flight = Flight.objects.get(pk=flight_id)
            obj.save()
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
        messages.error(request, 'Cannot delete ticket class. There are customer tickets for this class.')
        print('hi')
    else:
        ticket.delete()

    return redirect('manage_flight', flight_id=ticket.flight.pk)
