from django.shortcuts import render, redirect

from base_app.models import TicketCost
from base_app.forms import TicketCostForm


def index_page(request):
    ticket_costs = TicketCost.objects.all()

    return render(request, 'employees/manage_cost/index.html', {
        'ticket_costs': ticket_costs,
    })


def add_ticket_cost(request):
    form = TicketCostForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            
            return redirect('manage_cost_home')

    return render(request, 'employees/manage_cost/add_ticket_cost.html', {
        'form': form,
    })


def edit_ticket_cost(request, ticket_cost_id):
    ticket_cost = TicketCost.objects.get(id=ticket_cost_id)
    form = TicketCostForm(request.POST or None, instance=ticket_cost)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('manage_cost_home')

    return render(request, 'employees/manage_cost/edit_ticket_cost.html', {
        'form': form,
    })


def delete_ticket_cost(request, ticket_cost_id):
    ticket_cost = TicketCost.objects.get(id=ticket_cost_id)
    # TODO: check
    ticket_cost.delete()

    return redirect('manage_cost_home')
