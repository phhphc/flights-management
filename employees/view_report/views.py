from django.shortcuts import render
from base_app.models import Flight
from datetime import date

from .forms import *


def report_dashboard(request):

    todays_date = date.today()
    year = request.GET.get('year') or todays_date.year
    month = request.GET.get('month') or todays_date.month

    year_flights = Flight.objects.filter(departure_time__year=year)

    year_month_report = []
    for m in range(1, 13):
        month_flight = year_flights.filter(departure_time__month=m)

        month_total_ticket = sum([f.ticket_count for f in month_flight])
        if month_total_ticket:
            ticket_ratio = sum(
                [(f.ticket_ratio or 0)*f.ticket_count for f in month_flight]) / month_total_ticket
        else:
            ticket_ratio = 0

        year_month_report.append({
            'month': m,
            'flight_count': month_flight.count(),
            'revenue': sum([f.revenue for f in month_flight]),
            'ticket_ratio':  "%.2f%%" % (ticket_ratio*100),
        })

    form = MonthYearForm(initial={
        'year': year,
        'month': month,
    })

    month_flights_report = year_flights.filter(departure_time__month=month)
    for f in month_flights_report:
        f.ticket_ratio_str = "%.2f%%" % (f.ticket_ratio*100)

    return render(request, 'employees/view_report/index.html', {
        'form': form,
        'year': year,
        'month': month,
        'month_flights': month_flights_report,
        'year_month_report': year_month_report,
    })
