from django.contrib import admin
from .models import Airport, Flight , Passenger , Booking

class AirportAdmin(admin.ModelAdmin):
    list_display = ('code', 'city')
    search_fields = ('code', 'city')
    ordering = ('code', )

class FlightAdmin(admin.ModelAdmin):
    list_display = ('origin', 'destination')
    search_fields = ('origin', 'destination')
    ordering = ('-id',)

class PassengerAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username','user__email')
    ordering = ('-id',)

class BookingAdmin(admin.ModelAdmin):
    list_display = ('flight','booking_code')
    search_fields = ('flight','booking_code')
    ordering = ('-id',)

admin.site.register(Flight, FlightAdmin)
admin.site.register(Airport, AirportAdmin)
admin.site.register(Passenger, PassengerAdmin)
admin.site.register(Booking, BookingAdmin)
