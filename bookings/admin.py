from django.contrib import admin
from .models import Profile, TableBooking, Booking, Table, MenuItem


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user',)


admin.site.register(TableBooking)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('date', 'time', 'guests', 'your_name', 'email')
    search_fields = ('your_name', 'email')
    list_filter = ('date',)


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'seats')
    search_fields = ('table_number',)  
    list_filter = ('table_number', 'seats')


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'category')
    search_fields = ('name', 'description', 'price', 'category')
    list_filter = ('category',)