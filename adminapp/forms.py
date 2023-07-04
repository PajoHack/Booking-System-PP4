from django import forms
from bookings.models import MenuItem, Table

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ('name', 'description', 'price', 'category', 'image')
        

class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ('table_number', 'seats',)