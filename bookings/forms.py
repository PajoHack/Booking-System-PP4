from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from datetime import datetime, date, time, timedelta
from .models import Table, Booking, TableBooking

class BookingForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'id': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'text', 'id': 'datetimepicker'}))
    guests = forms.IntegerField(min_value=1, max_value=28, widget=forms.NumberInput(attrs={'min': '1', 'max': '28', 'id': 'guests'}))
    tables = forms.ModelMultipleChoiceField(queryset=Table.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'id': 'tables', 'class': 'table-checkbox'}))
    your_name = forms.CharField(label="Name on Booking", max_length=255)
    phone_number = forms.CharField(label="Phone Number", max_length=15)
    email = forms.EmailField(label="Email")
    
    class Meta:
        model = Booking
        fields = ['date', 'time', 'guests', 'tables', 'your_name', 'phone_number', 'email']
        
    def clean_time(self):
        booking_time = self.cleaned_data.get('time')
        if booking_time:
            # Booking time must be between 12:00 and 21:00.
            if booking_time < time(12, 0) or booking_time > time(21, 0):
                raise ValidationError('Booking time must be between 12 midday and 9pm.')
            
            # End time is implicitly 2 hours after start time.
            end_time = (datetime.combine(date.today(), booking_time) + timedelta(hours=2)).time()

            # Subtract one minute from the end time to ensure it aligns with the 30-minute booking steps.
            end_time = (datetime.combine(date.today(), end_time) - timedelta(minutes=1)).time()
            
            # End time should not be later than closing time.
            if end_time > time(21, 0):
                raise ValidationError('Booking time plus duration must not exceed closing time.')
        return booking_time

    
    def clean_date(self):
        booking_date = self.cleaned_data.get('date')
        if booking_date:
            if booking_date < datetime.date(datetime.now()):
                raise ValidationError('Booking date cannot be in the past.')
        return booking_date

    def clean(self):
    cleaned_data = super().clean()

    booking_time = cleaned_data.get('time')
    booking_date = cleaned_data.get('date')
    tables = cleaned_data.get('tables')

    if booking_time and booking_date and tables:
        for table in tables:
            latest_booking = Booking.objects.filter(
                tablebooking__table=table, 
                date=booking_date
            ).order_by('-time').first()

            if latest_booking:
                latest_booking_end_time = (datetime.combine(date.today(), latest_booking.time) + timedelta(hours=2)).time()
                min_start_time = (datetime.combine(date.today(), latest_booking_end_time) + timedelta(minutes=30)).time()

                if booking_time < min_start_time:
                    self.add_error('time', f'The selected time slot overlaps with a previous booking for Table {table.id}. Please choose a time later than {min_start_time.strftime("%H:%M")}.')
