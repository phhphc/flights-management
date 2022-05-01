from django.shortcuts import render, redirect


from .forms import *


def home_page(request):
    flights = Flight.objects.all().order_by('-pk')

    return render(request, 'employees/manage_ticket/index.html', {
        'flights': flights,
    })