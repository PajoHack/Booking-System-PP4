from django.urls import path
from . import views
from .views import check_availability


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('booking/', views.booking_view, name='booking'),
    path(
        'booking/edit/<int:pk>/',
        views.edit_booking_view,
        name='edit_booking'
    ),
    path(
        'booking/delete/<int:pk>/',
        views.delete_booking_view,
        name='delete_booking'
    ),
    path('menu/', views.menu_view, name="menu"),
    path('check_availability/', check_availability, name='check_availability'),
    path('gallery/', views.gallery_view, name='gallery'),
]
