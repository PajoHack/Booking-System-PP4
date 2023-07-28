from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import BookingForm
from .models import Booking, MenuItem, Table, TableBooking
from mailjet_rest import Client
import os
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta, datetime


def index(request):
    """
    View to display the homepage.
    """
    return render(request, 'index.html')


def login_view(request):
    """
    View for user login. Authenticates user and redirects to
    either admin home or profile depending on user type.
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username,
                            password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('adminapp:admin_home')
            else:
                return redirect('profile')
        else:
            return render(
                request, 'bookings/login.html',
                {'error': 'Invalid username or password'})
    else:
        return render(request, 'bookings/login.html')


def logout_view(request):
    """
    View for user logout. Redirects to login page after logout.
    """
    logout(request)
    return redirect('login')


def register(request):
    """
    View for user registration.
    Creates a new user and redirects to login page.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success
            (request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'bookings/register.html', {'form': form})


@login_required
def profile(request):
    """
    Profile view for the logged in user.
    Displays all bookings of the user.
    """
    now = timezone.localtime(timezone.now())
    bookings = Booking.objects.filter(
        user=request.user).order_by('-date', '-time')
    for booking in bookings:
        # Combine the date and time into a single datetime object.
        # This assumes that your Booking model has `date` and `time` fields.
        booking.datetime = timezone.make_aware(
            datetime.combine(booking.date, booking.time))

    return render(
        request, 'bookings/profile.html', {'bookings': bookings, 'now': now})


@login_required
def booking_view(request):
    """
    View for booking a table.
    Allows a logged in user to book a table and sends confirmation email.
    """
    if request.method == 'POST':
        form = BookingForm(request.POST)
        # print(f"Form is valid: {form.is_valid()}")
        # print(f"Form errors: {form.errors}")
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            form.save_m2m()

            # Send email confirmation
            api_key = os.getenv('MAILJET_API_KEY')
            api_secret = os.getenv('MAILJET_SECRET_KEY')
            mailjet = Client(auth=(api_key, api_secret), version='v3.1')

            admin_email = 'pajohack@gmail.com'

            data = {
                 'Messages': [
                    # Confirmation email to the user
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
                    },
                    # Notification email to the admin
                    {
                        'From': {
                            'Email': 'patrick.hackman@mail.com',
                            'Name': 'DeAngelo\'s',
                        },
                        'To': [
                            {
                                'Email': admin_email,
                                'Name': 'Admin',
                            }
                        ],
                        'TemplateID': 4936543,
                        'TemplateLanguage': True,
                        'Subject': 'New booking notification',
                        'Variables': {
                            'name': form.cleaned_data['your_name'],
                            'date': str(form.cleaned_data['date']),
                            'time': str(form.cleaned_data['time']),
                            'guests': str(form.cleaned_data['guests']),
                            'phone_number': form.cleaned_data['phone_number'],
                        },
                    },
                    ]
            }

            mailjet.send.create(data=data)

            return redirect('profile')
    else:
        form = BookingForm()

    return render(request, 'bookings/booking.html', {'form': form})


@login_required
def edit_booking_view(request, pk):
    """
    View for editing an existing booking.
    Allows a logged in user to modify a booking.
    """

    booking = get_object_or_404(Booking, id=pk, user=request.user)

    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.save()

            # Clear the current tables
            booking.tables.clear()
            # Add the selected tables
            for table in form.cleaned_data['tables']:
                booking.tables.add(table)

            return redirect('profile')
    else:
        form = BookingForm(instance=booking)

    context = {
        'form': form,
        'edit_mode': True,
        'booking': booking,
    }

    return render(request, 'bookings/booking.html', context)


@login_required
def delete_booking_view(request, pk):
    """
    View for deleting a booking.
    Allows a logged in user to delete a booking of their own.
    """
    booking = get_object_or_404(Booking, id=pk, user=request.user)

    if request.method == 'POST':
        booking.delete()
        return redirect('profile')

    return render(
        request, 'bookings/delete_booking.html', {'booking': booking})


def menu_view(request):
    """
    View to display the restaurant menu.
    Segregates menu items into starters, pizzas and pastas.
    """
    starters = MenuItem.objects.filter(category='ST')
    pizzas = MenuItem.objects.filter(category='PI')
    pastas = MenuItem.objects.filter(category='PA')

    context = {
        'starters': starters,
        'pizzas': pizzas,
        'pastas': pastas,
    }

    return render(request, 'bookings/menu.html', context)


def check_availability(request):
    """
    View to check table availability for a given date and time.
    """
    if request.method == 'GET':
        table_id = request.GET.get('table_id', None)
        date_str = request.GET.get('date', None)
        time_str = request.GET.get('time', None)
        booking_id = request.GET.get('booking_id', None)

        # print(f"table_id: {table_id}, date: {date_str}, time: {time_str}")

        if not table_id or not date_str or not time_str:
            return JsonResponse({'detail': 'Invalid request.'}, status=400)

        date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
        time = timezone.datetime.strptime(time_str, '%H:%M:%S').time()

        table = Table.objects.get(id=table_id)

        table_bookings = TableBooking.objects.filter(
            table=table, booking__date=date)

        overlap_exists = False
        booked_by_current_user = False
        for table_booking in table_bookings:
            booking_start = datetime.combine(date, table_booking.booking.time)
            booking_end = booking_start + timedelta(hours=1, minutes=30)

            requested_start = datetime.combine(date, time)
            requested_end = requested_start + timedelta(hours=1, minutes=30)

            if (booking_start <= requested_end) and \
               (requested_start <= booking_end):
                overlap_exists = True
                # Check if the booking is made by the current user
                if booking_id and str(table_booking.booking.id) == booking_id:
                    booked_by_current_user = True
                break

        if overlap_exists:
            return JsonResponse(
                {'available': False,
                 'booked_by_current_user': booked_by_current_user})
        else:
            return JsonResponse({'available': True})
    else:
        return JsonResponse({'detail': 'Invalid request method.'}, status=405)


def gallery_view(request):
    """
    The gallery view which renders the 'gallery.html' template.

    Args:
        request (HttpRequest): The request instance.

    Returns:
        HttpResponse: The response instance that renders the
        'gallery.html' template.
    """
    return render(request, 'bookings/gallery.html')


def handler500(request, *args, **argv):
    """
    The 500 error handler which renders the '500.html' template.

    Args:
        request (HttpRequest): The request instance.

    Returns:
        HttpResponse: The response instance that
        renders the '500.html' template with status code 500.
    """
    return render(request, '500.html', status=500)


def handler403(request, exception, *args, **argv):
    """
    The 403 error handler which renders the '403.html' template.

    Args:
        request (HttpRequest): The request instance.
        exception (Exception): The exception
        instance that triggered this handler.

    Returns:
        HttpResponse: The response instance
        that renders the '403.html' template with status code 403.
    """
    return render(request, '403.html', status=403)


def handler404(request, exception, *args, **argv):
    """
    The 404 error handler which renders the '404.html' template.

    Args:
        request (HttpRequest): The request instance.
        exception (Exception): The exception instance
        that triggered this handler.

    Returns:
        HttpResponse: The response instance that
        renders the '404.html' template with status code 404.
    """
    return render(request, '404.html', status=404)


def handler405(request, *args, **argv):
    """
    The 405 error handler which renders the '405.html' template.

    Args:
        request (HttpRequest): The request instance.

    Returns:
        HttpResponse: The response instance that
        renders the '405.html' template with status code 405.
    """
    return render(request, '405.html', status=405)
