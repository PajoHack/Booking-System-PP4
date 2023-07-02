from django.contrib import admin
from .models import Profile, TableBooking, Booking, Table


admin.site.register(Profile)

admin.site.register(TableBooking)

admin.site.register(Booking)

admin.site.register(Table)