from django import forms
from bookings.models import MenuItem, Table, Booking
from django.contrib.auth.models import User


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ('name', 'description', 'price', 'category', 'image')
        

class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ('table_number', 'seats',)
        

class BookingForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all())
    
    class Meta:
        model = Booking
        fields = ['date', 'time', 'guests', 'your_name', 'email', 'user',]