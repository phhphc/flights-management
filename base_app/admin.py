from django.contrib import admin

from .models import *


admin.site.register(CustomUser)
admin.site.register(Airport)
admin.site.register(TicketClass)
admin.site.register(TicketCost)
admin.site.register(Flight)
admin.site.register(IntermediateAirport)
admin.site.register(Ticket)