from django.shortcuts import render
from django.http import HttpResponse
from bookings.models import MenuItem


def index(request):
    return HttpResponse("Hello, world. You're at the adminapp index.")


def admin_home(request):
    return render(request, 'adminapp/admin_home.html')

def menu_list(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'adminapp/menu_list.html', {'menu_items': menu_items})

def menu_new(request):
    if request.method == "POST":
        menu_item = MenuItem(
            name = request.POST.get('name'),
            description = request.POST.get('description'),
            price = request.POST.get('price'),
            category = request.POST.get('category'),
            image = request.POST.get('image'),
        )
        menu_item.save()
        return redirect('adminapp:menu_edit', pk=menu_item.pk)
    return render(request, 'adminapp/menu_form.html')

def menu_edit(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)
    if request.method == "POST":
        menu_item.name = request.POST.get('name')
        menu_item.description = request.POST.get('description')
        menu_item.price = request.POST.get('price')
        menu_item.category = request.POST.get('category')
        menu_item.image = request.POST.get('image')
        menu_item.save()
        return redirect('adminapp:menu_edit', pk=menu_item.pk)
    return render(request, 'adminapp/menu_edit.html', {'menu_item': menu_item})


def menu_delete(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)
    if request.method == "POST":
        menu_item.delete()
        return redirect('adminapp:menu_list')
    return render(request, 'adminapp/menu_delete.html', {'menu_item': menu_item})