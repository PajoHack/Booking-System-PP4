from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import BookingForm
from .models import Booking, create_booking, MenuItem

# Create your views here.
def index(request):
    return render(request, 'index.html')


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
    # Redirect to a success page (for example, the login page).
    return redirect('login')

 
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login') # replace 'login' with the name of your login url
    else:
        form = UserCreationForm()
    return render(request, 'bookings/register.html', {'form': form})


@login_required
def profile(request):
    # get bookings for the current user
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'bookings/profile.html', {'bookings': bookings})


@login_required
def booking_view(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            form.save_m2m() # to save many-to-many data
            # Redirect to the user's profile page
            return redirect('profile')
    else:
        form = BookingForm()

    return render(request, 'bookings/booking.html', {'form': form})


@login_required
def edit_booking_view(request, pk):
    # Get the booking to update
    booking = get_object_or_404(Booking, id=pk, user=request.user)

    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            # Redirect to the user's profile page
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


# @login_required
# def delete_booking_view(request, pk):
#     booking = Booking.objects.get(pk=pk)
#     if request.user != booking.user:
#         return redirect('profile')
    
#     booking.delete()
#     return redirect('profile')


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