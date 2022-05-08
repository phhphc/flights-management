from django.db import models
from django.contrib.auth.models import User


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    id_card = models.CharField(max_length=20, blank=True)


class Airport(models.Model):
    code = models.CharField(max_length=10, unique=False)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TicketClass(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class TicketCost(models.Model):
    departure_airport = models.ForeignKey(
        Airport, on_delete=models.RESTRICT, related_name='tk_departure_airport')
    arrival_airport = models.ForeignKey(
        Airport, on_delete=models.RESTRICT, related_name='tk_arrival_airport', )
    ticket_class = models.ForeignKey(TicketClass, on_delete=models.RESTRICT)
    cost = models.DecimalField(decimal_places=0, max_digits=12)

    class Meta:
        unique_together = (('ticket_class', 'arrival_airport', 'departure_airport'),)


class Flight(models.Model):
    arrival_airport = models.ForeignKey(
        Airport, on_delete=models.RESTRICT, related_name='arrival_airport')
    departure_airport = models.ForeignKey(
        Airport, on_delete=models.RESTRICT, related_name='departure_airport')
    departure_time = models.DateTimeField()
    duration = models.DurationField()

    class Meta:
        ordering = ['departure_time']

    def __str__(self):
        return 'CB%06X' % self.id

    @property
    def revenue(self):
        return self.ticket_set.filter(status=3).aggregate(models.Sum('cost'))['cost__sum'] or 0

    @property
    def ticket_count(self):
        return self.numberofticket_set.aggregate(models.Sum('quantity'))['quantity__sum'] or 0

    @property
    def ticket_ratio(self):
        if self.ticket_count:
            return self.ticket_set.filter(status=3).count() / self.ticket_count
        return None


class NumberOfTicket(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    ticket_class = models.ForeignKey(TicketClass, on_delete=models.RESTRICT)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = (('ticket_class', 'flight'),)
        ordering = ['ticket_class']


class IntermediateAirport(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    airport = models.ForeignKey(Airport, on_delete=models.RESTRICT)
    stop_time = models.DurationField()
    notes = models.TextField(max_length=100)


class Ticket(models.Model):
    STATUS_LIST = models.IntegerChoices('Status', 'BOOK PAID DONE')

    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    ticket_class = models.ForeignKey(TicketClass, on_delete=models.RESTRICT)
    customer_name = models.CharField(max_length=100)
    customer_id_card = models.CharField(max_length=20)
    customer_phone = models.CharField(max_length=20)
    cost = models.DecimalField(decimal_places=0, max_digits=12)
    status = models.IntegerField(choices=STATUS_LIST.choices, default=1)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    employee_paid = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='employee_paid')

    class Meta:
        ordering = ['-id']

    @property
    def str_status(self):
        return self.STATUS_LIST(self.status).label

    def set_cost(self):
        self.cost = TicketCost.objects.get(
            ticket_class=self.ticket_class,
            arrival_airport=self.flight.arrival_airport,
            departure_airport=self.flight.departure_airport).cost


class Regulations(models.Model):
    flight_duration_min = models.DurationField()
    intermediate_airport_max = models.PositiveSmallIntegerField()
    intermediate_airport_time_min = models.DurationField()
    intermediate_airport_time_max = models.DurationField()
    book_ticket_before_min = models.DurationField()
    cancel_ticket_before_min = models.DurationField()
