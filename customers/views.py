from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from base_app.models import Flight, NumberOfTicket, TicketCost, IntermediateAirport, Ticket, Regulations
from base_app.forms import TicketForm, CustomUserForm


def home_page(request):
    flights: list[Flight] = Flight.objects.all()
    for i in range(len(flights)):
        total_seats = sum(
            [tk.quantity for tk in NumberOfTicket.objects.filter(flight__pk=flights[i].pk)])

        tickets: list[Ticket] = Ticket.objects.filter(flight__pk=flights[i].pk)

        flights[i].available_seats = total_seats - tickets.count()
        flights[i].booked_seats = tickets.filter(status=1).count()

    return render(request, 'customers/home.html', {
        'flights': flights
    })


def flight_detail(request, flight_id):
    flight: Flight = Flight.objects.get(pk=flight_id)
    intermediate_airports = IntermediateAirport.objects.filter(
        flight__pk=flight_id)

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

        ticket_details[i].available_seats = ticket_details[i].quantity - \
            tickets.count()

    return render(request, 'customers/flight_detail.html', {
        'flight': flight,
        'intermediate_airports': intermediate_airports,
        'ticket_details': ticket_details,
    })


@login_required(login_url='login')
def profile_page(request):

    form = CustomUserForm(request.POST or None,
                          instance=request.user.customuser)

    tickets: list[Ticket] = Ticket.objects.filter(user=request.user.id)

    if (request.method == 'POST'):
        if (form.is_valid()):
            form.save()
            messages.success(request, "Profile was updated!")

    return render(request, 'customers/profile.html', {
        'form': form,
        'tickets': tickets,
    })


@login_required(login_url='login')
def book_flight(request):
    customer = request.user.customuser
    form = TicketForm(data=request.POST or None,
                      user=request.user,
                      initial={
                          'flight': request.GET.get('flight'),
                          'ticket_class': request.GET.get('ticket_class'),
                          'customer_name': customer.name,
                          'customer_phone': customer.phone,
                          'customer_id_card': customer.id_card,
                      })

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Ticket was booked!")
            return redirect('profile')

    return render(request, 'customers/book_flight.html', {
        'form': form,
    })


@login_required(login_url='login')
def delete_book_flight(request, ticket_id):
    ticket = Ticket.objects.get(pk=ticket_id)

    cancel_ticket_before_min = Regulations.objects.get(
        pk=1).cancel_ticket_before_min
    departure_time = ticket.flight.departure_time
    # check time
    if departure_time - timezone.now() < cancel_ticket_before_min:
        messages.error(
            request, f"You can only cancel ticket before {departure_time-cancel_ticket_before_min}")
    # check status
    elif ticket.status != 1:
        messages.error(request, "You can only delete booked tickets!")
    #  check owner
    elif ticket.user == request.user:
        messages.success(request, "Ticket was deleted!")
        ticket.delete()

    return redirect('profile')
