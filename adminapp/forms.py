from django import forms
from bookings.models import MenuItem, Table, Booking
from django.contrib.auth.models import User


class MenuItemForm(forms.ModelForm):
    """
    Represents a form for creating or updating a menu item.

    The fields used are: 'name', 'description', 'price', 'category', 'image'.
    """
    class Meta:
        model = MenuItem
        fields = ('name', 'description', 'price', 'category', 'image')
        

class TableForm(forms.ModelForm):
    """
    Represents a form for creating or updating a table.

    The fields used are: 'table_number', 'seats'.
    """
    class Meta:
        model = Table
        fields = ('table_number', 'seats',)
        

class BookingForm(forms.ModelForm):
    """
    Represents a form for creating or updating a booking.

    The fields used are: 'date', 'time', 'guests', 'your_name', 'email', 'user'.

    Attributes:
        user (ModelChoiceField): The user associated with the booking.
    """
    user = forms.ModelChoiceField(queryset=User.objects.all())
    
    class Meta:
        model = Booking
        fields = ['date', 'time', 'guests', 'your_name', 'email', 'user',]