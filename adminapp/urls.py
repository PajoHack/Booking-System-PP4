from django.urls import path
from . import views

app_name = 'adminapp'

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.admin_home, name='admin_home'),
    path('menu/', views.menu_list, name='menu_list'),
    path('menu/new/', views.menu_new, name='menu_new'),
    path('menu/<int:pk>/edit/', views.menu_edit, name='menu_edit'),
    path('menu/<int:pk>/delete/', views.menu_delete, name='menu_delete'),
]
