from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from bookings.models import MenuItem, Table
from .forms import MenuItemForm, TableForm



def index(request):
    return HttpResponse("Hello, world. You're at the adminapp index.")


def admin_home(request):
    return render(request, 'adminapp/admin_home.html')

# menu views

def menu_list(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'adminapp/menu_list.html', {'menu_items': menu_items})


def menu_new(request):
    if request.method == "POST":
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            menu_item = form.save()
            return redirect('adminapp:menu_list')
    else:
        form = MenuItemForm()
    return render(request, 'adminapp/menu_form.html', {'form': form})


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


def menu_delete(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)
    if request.method == "POST":
        menu_item.delete()
        return redirect('adminapp:menu_list')
    return render(request, 'adminapp/menu_item_delete.html', {'menu_item': menu_item})


# table views

def table_list(request):
    tables = Table.objects.all()
    return render(request, 'adminapp/table_list.html', {'tables': tables})

# new table
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
def table_delete(request, pk):
    table = get_object_or_404(Table, pk=pk)
    if request.method == "POST":
        table.delete()
        return redirect('adminapp:table_list')
    return render(request, 'adminapp/table_confirm_delete.html', {'table': table})


# edit table
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