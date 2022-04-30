from django.contrib import admin
from sympy import Si

from .models import *


admin.site.register(CustomUser)
admin.site.register(Airport)
admin.site.register(TicketClass)
admin.site.register(TicketCost)
admin.site.register(Flight)
admin.site.register(NumberOfTicket)
admin.site.register(IntermediateAirport)
admin.site.register(Ticket)