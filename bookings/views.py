from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import BookingForm
from .models import Booking, create_booking, MenuItem
from mailjet_rest import Client
import os
from django.core.exceptions import PermissionDenied


def index(request):
    return render(request, 'index.html')


def admin_home2(request):
    return render(request, 'admin_home2.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('adminapp:admin_home')
            else:
                return redirect('profile')
        else:
            return render(request, 'bookings/login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'bookings/login.html')
    

def logout_view(request):
    logout(request)
    return redirect('login')

 
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'bookings/register.html', {'form': form})


@login_required
def profile(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'bookings/profile.html', {'bookings': bookings})


@login_required
def booking_view(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        print(f"Form is valid: {form.is_valid()}")
        print(f"Form errors: {form.errors}")
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            form.save_m2m()

            # Send email confirmation
            api_key = os.getenv('MAILJET_API_KEY')
            api_secret = os.getenv('MAILJET_SECRET_KEY')
            mailjet = Client(auth=(api_key, api_secret), version='v3.1')

            data = {
                'Messages': [
                    {
                        'From': {
                            'Email': 'patrick.hackman@mail.com',
                            'Name': 'DeAngelo\'s',
                        },
                        'To': [
                            {
                            'Email': form.cleaned_data['email'],
                            'Name': form.cleaned_data['your_name'],
                            }
                        ],
                        'TemplateID': 4936543,
                        'TemplateLanguage': True,
                        'Subject': 'Your booking confirmation',
                        'Variables': {
                            'name': form.cleaned_data['your_name'],
                            'date': str(form.cleaned_data['date']),
                            'time': str(form.cleaned_data['time']),
                            'guests': str(form.cleaned_data['guests']),
                            'phone_number': form.cleaned_data['phone_number'],
                        },
                    }
                ]
            }

            result = mailjet.send.create(data=data)
            # print(result.status_code)
            # print(result.json())

            return redirect('profile')
    else:
        form = BookingForm()

    return render(request, 'bookings/booking.html', {'form': form})


@login_required
def edit_booking_view(request, pk):

    booking = get_object_or_404(Booking, id=pk, user=request.user)

    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            booking = form.save(commit=False)  # save form, but don't commit yet
            booking.save()  # save the booking instance
            
            # Clear the current tables
            booking.tables.clear()
            # Add the selected tables
            for table in form.cleaned_data['tables']:
                booking.tables.add(table)

            return redirect('profile')
    else:
        form = BookingForm(instance=booking)

    return render(request, 'bookings/booking.html', {'form': form, 'edit_mode': True})


@login_required
def delete_booking_view(request, pk):
    booking = get_object_or_404(Booking, id=pk, user=request.user)
    
    if request.method == 'POST':
        booking.delete()
        return redirect('profile')
    
    return render(request, 'bookings/delete_booking.html', {'booking': booking})


def menu_view(request):
    starters = MenuItem.objects.filter(category='ST')
    pizzas = MenuItem.objects.filter(category='PI')
    pastas = MenuItem.objects.filter(category='PA')

    context = {
        'starters': starters,
        'pizzas': pizzas,
        'pastas': pastas,
    }

    return render(request, 'bookings/menu.html', context)


def handler500(request, *args, **argv):
    return render(request, '500.html', status=500)


def handler403(request, exception, *args, **argv):
    return render(request, '403.html', status=403)


def handler404(request, exception, *args, **argv):
    return render(request, '404.html', status=404)


def handler405(request, *args, **argv):
    return render(request, '405.html', status=405)


def error_500_view(request):
    raise Exception('This is a test exception')


def error_403_view(request):
    raise PermissionDenied