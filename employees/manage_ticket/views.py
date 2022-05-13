from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from base_app.models import Ticket
from base_app.filters import TicketFilter
from base_app.forms import TicketForm


def home_page(request):
    tickets = Ticket.objects.all()
    ticket_filter = TicketFilter(request.GET, queryset=tickets)
    tickets = ticket_filter.qs

    return render(request, 'employees/manage_ticket/index.html', {
        'ticket_filter': ticket_filter,
        'tickets': tickets,
    })


def add_ticket(request):
    form = TicketForm(data=request.POST or None,
                      employee=request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Ticket added')
            return redirect('manage_ticket_home')

    return render(request, 'employees/manage_ticket/add_ticket.html', {
        'form': form,
    })


def edit_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)

    # prevent exported tickets from being edited if they have been exported
    if ticket.status >= 3:
        messages.error(request, 'Cannot edit ticket after export')
        return redirect('manage_ticket_home')

    form = TicketForm(data=request.POST or None,
                      instance=ticket,
                      employee=request.user)
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Ticket edited')
            return redirect('manage_ticket_home')

    return render(request, 'employees/manage_ticket/edit_ticket.html', {
        'form': form,
    })


def delete_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)

    # prevent exported tickets from being deleted if they have been exported
    if ticket.status < 3:
        ticket.delete()
        messages.success(request, 'Ticket deleted')
    else:
        messages.error(request, 'Cannot delete ticket after export')

    return redirect('manage_ticket_home')


@login_required
def pay_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)

    # check if ticket is not already paid
    if ticket.status == 1:
        ticket.status = 2
        ticket.employee_paid = request.user
        ticket.save()
        messages.success(request, 'Ticket paid')
    else:
        messages.error(request, 'Ticket already paid')

    return redirect('manage_ticket_home')


def export_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)

    # ticket must be paid before export
    if ticket.status < 2:
        messages.error(request, 'Ticket has not been paid')
    else:
        ticket.status = 3
        ticket.save()
        messages.success(request, 'Ticket exported')

    return redirect('manage_ticket_home')
