from django.urls import path
from . import views

app_name = 'adminapp'

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.admin_home, name='admin_home'),
]
