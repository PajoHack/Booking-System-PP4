from django.shortcuts import render, get_object_or_404, redirect
from bookings.models import MenuItem, Table, Booking
from .forms import MenuItemForm, TableForm, BookingForm
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.paginator import Paginator


# def index(request):
#     return HttpResponse("Hello, world. You're at the adminapp index.")


def superuser_check(user):
    """Helper function to check if a user is a superuser."""
    return user.is_superuser


# menu views

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='adminapp:not_superuser')
def menu_list(request):
    """View to display a list of menu items."""
    menu_items = MenuItem.objects.all()
    return render(
        request, 'adminapp/menu_list.html', {'menu_items': menu_items})


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='adminapp:not_superuser')
def menu_new(request):
    """View to handle the creation of new menu items."""
    if request.method == "POST":
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('adminapp:menu_list')
    else:
        form = MenuItemForm()
    return render(request, 'adminapp/menu_form.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='adminapp:not_superuser')
def menu_edit(request, pk):
    """View to handle the editing of menu items."""
    menu_item = get_object_or_404(MenuItem, pk=pk)
    if request.method == "POST":
        form = MenuItemForm(request.POST, request.FILES, instance=menu_item)
        if form.is_valid():
            form.save()
            return redirect('adminapp:menu_list')
    else:
        form = MenuItemForm(instance=menu_item)
    return render(
        request, 'adminapp/menu_edit.html',
        {'form': form, 'menu_item': menu_item})


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='adminapp:not_superuser')
def menu_delete(request, pk):
    """View to handle the deletion of menu items."""
    menu_item = get_object_or_404(MenuItem, pk=pk)
    if request.method == "POST":
        menu_item.delete()
        return redirect('adminapp:menu_list')
    return render(
        request, 'adminapp/menu_item_delete.html', {'menu_item': menu_item})


# table views

# list of tables
@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='adminapp:not_superuser')
def table_list(request):
    """View to display a list of tables."""
    tables = Table.objects.all()
    return render(request, 'adminapp/table_list.html', {'tables': tables})


# new table
@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='adminapp:not_superuser')
def table_new(request):
    """View to handle the creation of new tables."""
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
    """View to handle the deletion of tables."""
    table = get_object_or_404(Table, pk=pk)
    if request.method == "POST":
        table.delete()
        return redirect('adminapp:table_list')
    return render(
        request, 'adminapp/table_confirm_delete.html', {'table': table})


# edit table
@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='adminapp:not_superuser')
def table_edit(request, pk):
    """View to handle the editing of tables."""
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
    """View to display a list of bookings."""
    bookings_list = Booking.objects.all().order_by('id')
    paginator = Paginator(bookings_list, 10)  # Show 10 bookings per page.

    page_number = request.GET.get('page')
    bookings = paginator.get_page(page_number)

    return render(
        request, 'adminapp/booking_list.html', {'bookings': bookings})


# new booking
@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='adminapp:not_superuser')
def booking_new(request):
    """View to handle the creation of new bookings."""
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user_id = form.cleaned_data['user'].id
            booking.save()
            return redirect('adminapp:booking_list')
    else:
        form = BookingForm()
    return render(
        request, 'adminapp/booking_form.html',
        {'form': form, 'form_type': 'New'})


# edit booking
@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='adminapp:not_superuser')
def booking_edit(request, pk):
    """View to handle the editing of bookings."""
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == "POST":
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            booking = form.save()
            return redirect('adminapp:booking_list')
    else:
        form = BookingForm(instance=booking)
    return render(
        request, 'adminapp/booking_form.html',
        {'form': form, 'form_type': 'Edit'})


# delete booking
@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='adminapp:not_superuser')
def booking_delete(request, pk):
    """View to handle the deletion of bookings."""
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        booking.delete()
        return redirect('adminapp:booking_list')
    return render(
        request, 'adminapp/booking_confirm_delete.html',
        {'object': booking})


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='adminapp:not_superuser')
def admin_home(request):
    """View to handle the admin homepage,
    showing counts of bookings, menu items, and tables.
    """
    booking_count = Booking.objects.count()
    menu_item_count = MenuItem.objects.count()
    table_count = Table.objects.count()

    context = {
        'booking_count': booking_count,
        'menu_item_count': menu_item_count,
        'table_count': table_count,
    }

    return render(request, 'adminapp/admin_home.html', context)


def not_superuser(request):
    """View to handle the page that is
    shown when the user is not a superuser."""
    return render(request, 'adminapp/not_superuser.html')
