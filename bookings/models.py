from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from cloudinary.models import CloudinaryField


class Table(models.Model):
    """
    Represents a table in the restaurant.
    
    Attributes:
        table_number (IntegerField): The table number in the restaurant.
        seats (IntegerField): The number of seats at the table.
    """
    table_number = models.IntegerField(unique=True)
    seats = models.IntegerField()
    
    def __str__(self):
        return f"Table {self.table_number} has {self.seats} seats"


class Booking(models.Model):
    """
    Represents a booking made by a user.

    Attributes:
        user (ForeignKey): The user who made the booking.
        date (DateField): The date of the booking.
        time (TimeField): The time of the booking.
        guests (IntegerField): The number of guests for the booking.
        your_name (CharField): The name of the person making the booking.
        email (EmailField): The email address of the person making the booking.
        phone_number (CharField): The contact phone number of the person making the booking.
        created_at (DateTimeField): The date and time the booking was made.
        tables (ManyToManyField): The tables booked.
    """
    user = models.ForeignKey(User, related_name='bookings', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    guests = models.IntegerField()
    your_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    tables = models.ManyToManyField(Table, through='TableBooking')


class TableBooking(models.Model):
    """
    Intermediate model for ManyToMany relationship between Booking and Table.

    Attributes:
        table (ForeignKey): The table being booked.
        booking (ForeignKey): The booking the table is for.
    """
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('table', 'booking')



@transaction.atomic
def create_booking(user, date, time, guests, your_name, email, tables):
    """
    Create a booking and associated table bookings atomically.

    Args:
        user (User): The user making the booking.
        date (datetime.date): The date of the booking.
        time (datetime.time): The time of the booking.
        guests (int): The number of guests for the booking.
        your_name (str): The name of the person making the booking.
        email (str): The email address of the person making the booking.
        tables (list): The tables being booked.

    Returns:
        None
    """
    booking = Booking.objects.create(user=user, date=date, time=time, guests=guests, your_name=your_name, email=email)
    for table in tables:
        TableBooking.objects.create(table=table, booking=booking)


class MenuItem(models.Model):
    """
    Represents a menu item in the restaurant.

    Attributes:
        name (CharField): The name of the menu item.
        description (TextField): A short description of the item.
        price (DecimalField): The price of the menu item.
        category (CharField): The category of the menu item (e.g., starters, pizza, pasta).
        image (CloudinaryField): An image of the menu item.
    """
    CATEGORY_CHOICES = [
        ('ST', 'Starters'),
        ('PI', 'Pizza'),
        ('PA', 'Pasta'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default='ST')
    image = CloudinaryField('image', default='https://res.cloudinary.com/dpwp5cavi/image/upload/v1687277051/menu_pic_q2kjau.jpg')

    def __str__(self):
        return self.name
  

class Profile(models.Model):
    """
    Represents a user profile.

    Attributes:
        user (OneToOneField): The user the profile belongs to.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create a user profile when a user is created.

    Args:
        sender (Model): The model class. 
        instance (Model instance): The actual instance being saved.
        created (bool): True if a new record was created.

    Returns:
        None
    """
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Save a user profile when a user is saved.

    Args:
        sender (Model): The model class. 
        instance (Model instance): The actual instance being saved.

    Returns:
        None
    """
    instance.profile.save()

