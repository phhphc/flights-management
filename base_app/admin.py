from django.contrib import admin

from .models import Country, CustomUser, City


admin.site.register(CustomUser)
admin.site.register(Country)
admin.site.register(City)
