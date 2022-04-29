from django.db import models
from django.contrib.auth.models import User


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
    cost = models.IntegerField(default=0)

    class Meta:
        unique_together = (('ticket_class', 'dst_airport', 'src_airport'),)


class Flight(models.Model):
    dst_airport = models.ForeignKey(
        Airport, on_delete=models.RESTRICT, related_name='dst_airport')
    src_airport = models.ForeignKey(
        Airport, on_delete=models.RESTRICT, related_name='src_airport')
    flight_time = models.DateTimeField()
    duration = models.DurationField()
    
    def __str__(self):
        return 'CB%05d'%self.id


class NumberOfTicket(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    ticket_class = models.ForeignKey(TicketClass, on_delete=models.RESTRICT)
    quantity = models.IntegerField(default=0)

    class Meta:
        unique_together = (('ticket_class', 'flight'),)


class IntermediateAirport(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    airport = models.ForeignKey(Airport, on_delete=models.RESTRICT)
    stop_time = models.DurationField()
    notes = models.TextField(max_length=100)

class Ticket(models.Model):
    STATUS_LIST = models.IntegerChoices('Status', 'BOOK PAID')
    
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    customer_id_number = models.CharField(max_length=20)
    customer_phone = models.CharField(max_length=20)
    ticket_class = models.ForeignKey(TicketClass, on_delete=models.RESTRICT)
    status = models.IntegerField(choices=STATUS_LIST.choices, default=0)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)