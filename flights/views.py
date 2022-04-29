from django.shortcuts import render
from models.models import Flight, NumberOfTicket, TicketCost


from .forms import *


def home_page(request):
    flights: list[Flight] = Flight.objects.all()
    for i in range(len(flights)):
        total_seats = sum(
            [tk.quantity for tk in NumberOfTicket.objects.filter(flight__pk=flights[i].pk)])
        sold_seats = 0

        flights[i].available_seats = total_seats - sold_seats
        flights[i].booked_seats = 0

    return render(request, 'flights/home.html', {
        'flights': flights
    })


def flight_detail(request, flight_id):
    flight: Flight = Flight.objects.get(pk=flight_id)
    ticket_costs: list[TicketCost] = TicketCost.objects.filter(
        dst_airport__pk=flight.dst_airport.pk, src_airport__pk=flight.src_airport.pk)
    ticket_numbers: list[NumberOfTicket] = NumberOfTicket.objects.filter(
        flight__pk=flight.pk)
    

    return render(request, 'flights/flight_detail.html', {
        'flight': flight,
        'ticket_costs': ticket_costs,
        'ticket_numbers': ticket_numbers
    })


def book_flight(request):
    form = BookTicketForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            if request.user.is_authenticated:
                obj.user = request.user
            obj.save()
            return render(request, 'flights/book_success.html')

    return render(request, 'flights/book_flight.html', {
        'form': form,
    })
