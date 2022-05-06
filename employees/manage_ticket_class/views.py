from django.shortcuts import render, redirect

from base_app.models import TicketClass
from base_app.forms import TicketClassForm


def index_page(request):
    ticket_classes = TicketClass.objects.all()

    return render(request, 'employees/manage_ticket_class/index.html', {
        'ticket_classes': ticket_classes,
    })


def add_ticket_class(request):
    form = TicketClassForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            
            return redirect('manage_ticket_class_home')

    return render(request, 'employees/manage_ticket_class/add_ticket_class.html', {
        'form': form,
    })


def edit_ticket_class(request, ticket_class_id):
    ticket_class = TicketClass.objects.get(id=ticket_class_id)
    form = TicketClassForm(request.POST or None, instance=ticket_class)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('manage_ticket_class_home')

    return render(request, 'employees/manage_ticket_class/edit_ticket_class.html', {
        'form': form,
    })


def delete_ticket_class(request, ticket_class_id):
    ticket_class = TicketClass.objects.get(id=ticket_class_id)
    # TODO: check
    ticket_class.delete()

    return redirect('manage_ticket_class_home')
