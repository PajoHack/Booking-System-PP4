from django.contrib import admin
from .models import Profile, TableBooking, Booking, Table, MenuItem


admin.site.register(Profile)

admin.site.register(TableBooking)

admin.site.register(Booking)

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'seats')
    search_fields = ('table_number',)  
    list_filter = ('table_number', 'seats')

admin.site.register(MenuItem)