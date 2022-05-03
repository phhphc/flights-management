from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from models.models import Ticket

from .forms import *


def home_page(request):
    tickets = Ticket.objects.all()

    return render(request, 'employees/manage_ticket/index.html', {
        'tickets': tickets,
    })


def add_ticket(request):
    form = TicketForm(request.POST or None)
    # TODO: check if ticket cost exists
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            obj.set_cost()
            obj.status = 2
            obj.employee_paid = request.user
            obj.save()
            return redirect('manage_ticket_home')

    return render(request, 'employees/manage_ticket/add_ticket.html', {
        'form': form,
    })


def edit_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    # TODO: check if ticket.status != 3 (exported)
    form = TicketForm(request.POST or None, instance=ticket)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('manage_ticket_home')

    return render(request, 'employees/manage_ticket/edit_ticket.html', {
        'form': form,
    })


def delete_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    # TODO: check if ticket.status != 3 (exported)
    ticket.delete()

    return redirect('manage_ticket_home')


@login_required
def pay_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    # TODO: check if ticket.status == 1 (booked)
    ticket.status = 2
    ticket.employee_paid = request.user
    ticket.save()

    return redirect('manage_ticket_home')


def export_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    # TODO: check if ticket.status == 2 (paid)
    ticket.status = 3
    ticket.save()

    return redirect('manage_ticket_home')
