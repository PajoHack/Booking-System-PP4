from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from bookings.models import MenuItem, Table, Booking
from .forms import MenuItemForm, TableForm, BookingForm
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.paginator import Paginator


def index(request):
    return HttpResponse("Hello, world. You're at the adminapp index.")


def superuser_check(user):
    return user.is_superuser


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='adminapp:not_superuser')
def admin_home(request):
    return render(request, 'adminapp/admin_home.html')


def not_superuser(request):
    return render(request, 'adminapp/not_superuser.html')


# menu views

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='adminapp:not_superuser')
def menu_list(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'adminapp/menu_list.html', {'menu_items': menu_items})


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='adminapp:not_superuser')
def menu_new(request):
    if request.method == "POST":
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            menu_item = form.save()
            return redirect('adminapp:menu_list')
    else:
        form = MenuItemForm()
    return render(request, 'adminapp/menu_form.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='adminapp:not_superuser')
def menu_edit(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)
    if request.method == "POST":
        form = MenuItemForm(request.POST, request.FILES, instance=menu_item)
        if form.is_valid():
            form.save()
            return redirect('adminapp:menu_list')
    else:
        form = MenuItemForm(instance=menu_item)
    return render(request, 'adminapp/menu_edit.html', {'form': form, 'menu_item': menu_item})


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='adminapp:not_superuser')
def menu_delete(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)
    if request.method == "POST":
        menu_item.delete()
        return redirect('adminapp:menu_list')
    return render(request, 'adminapp/menu_item_delete.html', {'menu_item': menu_item})


# table views

# list of tables
@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='adminapp:not_superuser')
def table_list(request):
    tables = Table.objects.all()
    return render(request, 'adminapp/table_list.html', {'tables': tables})

# new table
@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='adminapp:not_superuser')
def table_new(request):
    if request.method == "POST":
        form = TableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminapp:table_list')
    else:
        form = TableForm()
    return render(request, 'adminapp/table_form.html', {'form': form})


# delete table
@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='adminapp:not_superuser')
def table_delete(request, pk):
    table = get_object_or_404(Table, pk=pk)
    if request.method == "POST":
        table.delete()
        return redirect('adminapp:table_list')
    return render(request, 'adminapp/table_confirm_delete.html', {'table': table})


# edit table
@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='adminapp:not_superuser')
def table_edit(request, pk):
    table = get_object_or_404(Table, pk=pk)

    if request.method == 'POST':
        form = TableForm(request.POST, instance=table)
        if form.is_valid():
            form.save()
            return redirect('adminapp:table_list')
    else:
        form = TableForm(instance=table)

    return render(request, 'adminapp/table_edit.html', {'form': form})


# booking views

# list of bookings
@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='adminapp:not_superuser')
def booking_list(request):
    bookings_list = Booking.objects.all()
    paginator = Paginator(bookings_list, 10)  # Show 10 bookings per page.

    page_number = request.GET.get('page')
    bookings = paginator.get_page(page_number)

    return render(request, 'adminapp/booking_list.html', {'bookings': bookings})

# new booking
@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='adminapp:not_superuser')
def booking_new(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user_id = form.cleaned_data['user'].id
            booking.save()
            return redirect('adminapp:booking_list')
    else:
        form = BookingForm()
    return render(request, 'adminapp/booking_form.html', {'form': form, 'form_type': 'New'})

# edit booking
@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='adminapp:not_superuser')
def booking_edit(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == "POST":
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            booking = form.save()
            return redirect('adminapp:booking_list')
    else:
        form = BookingForm(instance=booking)
    return render(request, 'adminapp/booking_form.html', {'form': form, 'form_type': 'Edit'})

# delete booking
@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='adminapp:not_superuser')
def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        booking.delete()
        return redirect('adminapp:booking_list')
    return render(request, 'adminapp/booking_confirm_delete.html', {'object': booking})