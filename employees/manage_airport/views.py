from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib import messages

from base_app.models import Airport
from base_app.forms import AirportForm


def index_page(request):
    airports = Airport.objects.all()

    return render(request, 'employees/manage_airport/index.html', {
        'airports': airports,
    })


def add_airport(request):
    form = AirportForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()

            return redirect('manage_airport_home')

    return render(request, 'employees/manage_airport/add_airport.html', {
        'form': form,
    })


def edit_airport(request, airport_id):
    airport = Airport.objects.get(id=airport_id)
    form = AirportForm(request.POST or None, instance=airport)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('manage_airport_home')

    return render(request, 'employees/manage_airport/edit_airport.html', {
        'form': form,
    })


def delete_airport(request, airport_id):
    airport = Airport.objects.get(id=airport_id)
    
    try:
        airport.delete()
    except IntegrityError:
        messages.error(
            request, 'Cannot delete this airport because it is used by some flights !')

    return redirect('manage_airport_home')
