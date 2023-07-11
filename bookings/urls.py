from django.urls import path
from . import views
from .views import error_500_view


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('booking/', views.booking_view, name='booking'),
    path('booking/edit/<int:pk>/', views.edit_booking_view, name='edit_booking'),
    path('booking/delete/<int:pk>/', views.delete_booking_view, name='delete_booking'),
    path('menu/', views.menu_view, name="menu"),
    path('500/', error_500_view, name='500_error'),
    # path('403/', error_403_view, name='403_error'),
]