from django.db import models
from django.contrib.auth.models import User


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    id_card = models.CharField(max_length=20, blank=True)


class Airport(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TicketClass(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class TicketCost(models.Model):
    ticket_class = models.ForeignKey(TicketClass, on_delete=models.RESTRICT)
    dst_airport = models.ForeignKey(
        Airport, on_delete=models.RESTRICT, related_name='tk_dst_airport', )
    src_airport = models.ForeignKey(
        Airport, on_delete=models.RESTRICT, related_name='tk_src_airport')
    cost = models.DecimalField(decimal_places=0, max_digits=12)

    class Meta:
        unique_together = (('ticket_class', 'dst_airport', 'src_airport'),)


class Flight(models.Model):
    dst_airport = models.ForeignKey(
        Airport, on_delete=models.RESTRICT, related_name='dst_airport')
    src_airport = models.ForeignKey(
        Airport, on_delete=models.RESTRICT, related_name='src_airport')
    flight_time = models.DateTimeField()
    duration = models.DurationField()

    class Meta:
        ordering = ['flight_time']

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
    sequence = models.PositiveIntegerField()
    stop_time = models.DurationField()
    notes = models.TextField(max_length=100)

    class Meta:
        unique_together = (('flight', 'airport'),)
        ordering = ['sequence']


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
            dst_airport=self.flight.dst_airport,
            src_airport=self.flight.src_airport).cost
