from django.shortcuts import render
from models.models import Flight, NumberOfTicket, TicketCost
from django.contrib.auth.decorators import login_required


from .forms import *


def home_page(request):
    flights: list[Flight] = Flight.objects.all()
    for i in range(len(flights)):
        total_seats = sum(
            [tk.quantity for tk in NumberOfTicket.objects.filter(flight__pk=flights[i].pk)])

        tickets: list[Ticket] = Ticket.objects.filter(flight__pk=flights[i].pk)

        flights[i].available_seats = total_seats - tickets.count()
        flights[i].booked_seats = tickets.filter(status=1).count()

    return render(request, 'flights/home.html', {
        'flights': flights
    })


def flight_detail(request, flight_id):
    flight: Flight = Flight.objects.get(pk=flight_id)

    ticket_details = NumberOfTicket.objects.filter(flight__pk=flight_id)
    for i in range(len(ticket_details)):
        ticket_details[i].cost = TicketCost.objects.get(
            dst_airport__pk=flight.dst_airport.pk,
            src_airport__pk=flight.src_airport.pk,
            ticket_class=ticket_details[i].ticket_class).cost

        tickets = Ticket.objects.filter(
            flight__pk=flight.pk,
            ticket_class=ticket_details[i].ticket_class)

        ticket_details[i].booked_count = tickets.filter(
            status=1).count()

        ticket_details[i].available_seats = ticket_details[i].quantity - tickets.count()

    return render(request, 'flights/flight_detail.html', {
        'flight': flight,
        'ticket_details': ticket_details,
    })


@login_required(login_url='login')
def book_flight(request):
    customer = request.user.customuser
    form = BookTicketForm(request.POST or None, initial={
        'flight': request.GET.get('flight'),
        'ticket_class': request.GET.get('ticket_class'),
        'customer_name': customer.name,
        'customer_phone': customer.phone,
        'customer_id_card': customer.id_card,
    })

    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            # TODO: Check if ticket seat is available
            obj.user = request.user
            obj.save()
            return render(request, 'flights/book_success.html')

    return render(request, 'flights/book_flight.html', {
        'form': form,
    })
