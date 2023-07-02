from django import forms
from .models import Table, Booking


class BookingForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'id': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    guests = forms.IntegerField()
    table = forms.ModelMultipleChoiceField(queryset=Table.objects.all(), widget=forms.CheckboxSelectMultiple)
    name_on_booking = forms.CharField(label="Name on Booking", max_length=255)
    phone_number = forms.CharField(label="Phone Number", max_length=15)
    email = forms.EmailField(label="Email")
    
    class Meta:
        model = Booking
        fields = ['date', 'time', 'guests', 'table', 'name_on_booking', 'phone_number', 'email']

