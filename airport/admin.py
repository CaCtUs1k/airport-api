from django.contrib import admin

from airport.models import (
    AirplaneType,
    Airplane,
    Crew,
    Airport,
    Route,
    Flight,
    Order,
    Ticket,
)

# Register your models here.
admin.site.register(AirplaneType)
admin.site.register(Airplane)
admin.site.register(Crew)
admin.site.register(Airport)
admin.site.register(Route)
admin.site.register(Flight)
admin.site.register(Order)
admin.site.register(Ticket)
