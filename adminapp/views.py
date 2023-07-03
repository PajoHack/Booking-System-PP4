from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the adminapp index.")


def admin_home(request):
    return render(request, 'adminapp/admin_home.html')

