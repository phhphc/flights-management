from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from matplotlib.axis import Tick

from base_app.models import Flight, FlightTicket, IntermediateAirport, Ticket, Regulations
from base_app.forms import TicketForm, CustomUserForm
from base_app.filters import FlightFilter, TicketFilter
from payments.forms import PaymentForm

from .forms import *


def home_page(request):
    flights: list[Flight] = Flight.objects.all()

    query = request.GET.copy()
    if 'departure_time__date__gte' not in query or not query['departure_time__date__gte']:
        query['departure_time__date__gte'] = timezone.now().date()

    flight_filter: FlightFilter = FlightFilter(query, queryset=flights)
    flights = flight_filter.qs[:20]

    for i in range(len(flights)):
        total_seats = sum(
            [tk.quantity for tk in FlightTicket.objects.filter(flight__pk=flights[i].pk)])

        tickets: list[Ticket] = Ticket.objects.filter(
            flight_ticket__flight__pk=flights[i].pk)

        flights[i].available_seats = total_seats - tickets.count()
        flights[i].booked_seats = tickets.filter(status=1).count()

    return render(request, 'customers/home.html', {
        'flights': flights,
        "flight_filter": flight_filter,
    })


def flight_detail(request, flight_id):
    flight: Flight = Flight.objects.get(pk=flight_id)
    intermediate_airports = IntermediateAirport.objects.filter(
        flight__pk=flight_id)

    flight_tickets = FlightTicket.objects.filter(flight__pk=flight_id)
    for ft in flight_tickets:
        tickets = ft.ticket_set.all()
        ft.booked_count = tickets.filter(status=1).count()
        ft.available_seats = ft.quantity - tickets.count()

    return render(request, 'customers/flight_detail.html', {
        'flight': flight,
        'intermediate_airports': intermediate_airports,
        'flight_tickets': flight_tickets,
    })


@login_required(login_url='login')
def profile_page(request):

    form = CustomUserForm(request.POST or None,
                          instance=request.user.customuser)
    tickets = Ticket.objects.filter(user=request.user.id)
    ticket_filter = TicketFilter(request.GET, queryset=tickets)
    tickets = ticket_filter.qs

    if (request.method == 'POST'):
        if (form.is_valid()):
            form.save()
            messages.success(request, "Profile was updated!")

    return render(request, 'customers/profile.html', {
        'form': form,
        'tickets': tickets,
        'ticket_filter': ticket_filter,
    })


def book_flight(request):
    if request.user.is_authenticated:
        customer = request.user.customuser
        initial = {
            'flight': request.GET.get('flight'),
            'ticket_class': request.GET.get('ticket_class'),
            'customer_name': customer.name,
            'customer_phone': customer.phone,
            'customer_id_card': customer.id_card,
        }
    else:
        initial = {
            'flight': request.GET.get('flight'),
            'ticket_class': request.GET.get('ticket_class'),
        }

    form = TicketForm(data=request.POST or None,
                      user=request.user,
                      initial=initial)

    payment = PaymentForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():

            if payment.is_empty():
                obj = form.save(commit=False)
                obj.seat_position = None
                obj.save()
                messages.success(request, "Ticket was booked!")
                return redirect('home')

            elif payment.is_valid():
                payment.save()
                obj = form.save(commit=False)
                obj.status = 2
                obj.save()
                messages.success(request, "Ticket was paid!")
                return redirect('home')

    return render(request, 'customers/book_flight.html', {
        'form': form,
        'payment': payment,
    })


def book_flight_confirm(request, ticket_id):

    payment = PaymentForm(request.POST or None)
    ticket = Ticket.objects.get(pk=ticket_id)

    if request.method == 'POST':
        if payment.is_valid():
            try:
                payment.save()
                messages.success(request, "Payment was successful!")
                return redirect('profile')
            except:
                messages.error(request, "Error while processing payment!")

    return render(request, 'customers/book_flight_confirm.html', {
        'payment': payment,
        'ticket': ticket,
    })


def edit_ticket_customer(request, ticket_id):
    form = CustomerTicketForm(data=request.POST or None,
                              instance=Ticket.objects.get(pk=ticket_id))

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Ticket was updated!")
            return redirect('profile')

    return render(request, 'customers/edit_ticket_customer.html', {
        'form': form,
    })


@login_required(login_url='login')
def delete_book_flight(request, ticket_id):
    ticket = Ticket.objects.get(pk=ticket_id)

    cancel_ticket_before_min = Regulations.objects.get(
        pk=1).cancel_ticket_before_min
    departure_time = ticket.flight_ticket.flight.departure_time
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
