from django.urls import path
from . import views

app_name = 'adminapp'

urlpatterns = [
    path('', views.admin_home, name='admin_home'),
    path('adminapps2/', views.admin_home2, name='admin_home2'),
    # menu urls
    path('menu/', views.menu_list, name='menu_list'),
    path('menu/new/', views.menu_new, name='menu_new'),
    path('menu/<int:pk>/edit/', views.menu_edit, name='menu_edit'),
    path('menu/<int:pk>/delete/', views.menu_delete, name='menu_delete'),
    # table urls
    path('tables/', views.table_list, name='table_list'),
    path('tables/new/', views.table_new, name='table_new'),
    path('tables/<int:pk>/delete/', views.table_delete, name='table_delete'),
    path('table/<int:pk>/edit/', views.table_edit, name='table_edit'),
    # bookings urls
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/new/', views.booking_new, name='booking_new'),
    path('bookings/<int:pk>/edit/', views.booking_edit, name='booking_edit'),
    path('bookings/<int:pk>/delete/', views.booking_delete, name='booking_delete'),
    
    path('not_superuser/', views.not_superuser, name='not_superuser'),
]

