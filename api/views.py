from django.http import JsonResponse

from base_app.models import FlightTicket


def flight_seat_list(request, flight_id, ticket_class_id):

    flight_ticket = FlightTicket.objects.get(
        flight__id=flight_id, ticket_class__id=ticket_class_id)
    seats = [i[0] for i in flight_ticket.ticket_set.filter(seat_position__isnull=False).values_list('seat_position')]

    return JsonResponse({
        'total': flight_ticket.quantity,
        'bookedSeats': seats,
    })
