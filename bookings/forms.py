from django import forms
from .models import Table, Booking
from django.core.exceptions import ValidationError
from datetime import datetime, time


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
        
    def clean_time(self):
        booking_time = self.cleaned_data.get('time')
        if booking_time:
            if booking_time < time(12, 0) or booking_time > time(21, 0):
                raise ValidationError('Booking time must be between 12 midday and 9pm.')
        return booking_time
    
    def clean_date(self):
        booking_date = self.cleaned_data.get('date')
        if booking_date:
            if booking_date < datetime.date(datetime.now()):
                raise ValidationError('Booking date cannot be in the past.')
        return booking_date


