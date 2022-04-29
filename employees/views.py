from django.shortcuts import render, redirect


from .forms import *


def home_page(request):
    flights = Flight.objects.all().order_by('-pk')

    return render(request, 'employees/home.html', {
        'flights': flights,
    })


def manage_flight(request, flight_id):
    flight = Flight.objects.get(pk=flight_id)
    intermediate_airports = IntermediateAirport.objects.filter(flight=flight).order_by('sequence')
    tickets = NumberOfTicket.objects.filter(flight__pk=flight_id)

    return render(request, 'employees/manage_flight.html', {
        'flight': flight,
        'intermediate_airports': intermediate_airports,
        'tickets': tickets,
    })


def add_flight(request):
    form = FlightForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            obj = form.save()
            return redirect(f'/employee/manage-flight/{obj.pk}')

    return render(request, 'employees/add_flight.html', {
        'form': form,
    })


def edit_flight(request, flight_id):
    flight = Flight.objects.get(pk=flight_id)
    form = FlightForm(request.POST or None, instance=flight)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(f'/employee/manage-flight/{flight_id}')

    return render(request, 'employees/edit_flight.html', {
        'form': form,
        'flight_id': flight_id,
    })


def delete_flight(request, flight_id):
    flight = Flight.objects.get(pk=flight_id)
    flight.delete()

    return redirect('/employee/')


def add_intermediate_airport(request, flight_id):
    form = IntermediateAirportForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            obj.flight = Flight.objects.get(pk=flight_id)
            obj.save()
            return redirect(f'/employee/manage-flight/{flight_id}')

    return render(request, 'employees/add_intermediate_aitport.html', {
        'form': form,
        'flight_id': flight_id,
    })


def edit_intermediate_airport(request, intermediate_airport_id):
    airport = IntermediateAirport.objects.get(pk=intermediate_airport_id)
    form = IntermediateAirportForm(request.POST or None, instance=airport)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(f'/employee/manage-flight/{airport.flight.pk}')

    return render(request, 'employees/edit_intermediate_airport.html', {
        'form': form,
        'flight_id': airport.flight.pk,
    })


def delete_intermediate_airport(request, intermediate_airport_id):
    airport = IntermediateAirport.objects.get(pk=intermediate_airport_id)
    airport.delete()

    return redirect(f'/employee/manage-flight/{airport.flight.pk}')


def add_ticket(request, flight_id):
    form = NumberOfTicketForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            obj.flight = Flight.objects.get(pk=flight_id)
            obj.save()
            return redirect(f'/employee/manage-flight/{flight_id}')

    return render(request, 'employees/add_ticket.html', {
        'form': form,
        'flight_id': flight_id,
    })


def edit_ticket(request, ticket_id):
    ticket = NumberOfTicket.objects.get(pk=ticket_id)
    form = NumberOfTicketForm(request.POST or None, instance=ticket)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(f'/employee/manage-flight/{ticket.flight.pk}')

    return render(request, 'employees/edit_ticket.html', {
        'form': form,
        'flight_id': ticket.flight.pk,
    })


def delete_ticket(request, ticket_id):
    ticket = NumberOfTicket.objects.get(pk=ticket_id)
    ticket.delete()

    return redirect(f'/employee/manage-flight/{ticket.flight.pk}')
