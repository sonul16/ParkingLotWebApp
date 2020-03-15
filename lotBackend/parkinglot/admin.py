from django.contrib import admin

# Register your models here.
from parkinglot.models import ParkingLot, ParkingSlot, Customer, ParkingSlotReservation

admin.site.register(ParkingLot)
admin.site.register(ParkingSlot)
admin.site.register(Customer)
admin.site.register(ParkingSlotReservation)



