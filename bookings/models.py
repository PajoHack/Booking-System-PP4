from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from cloudinary.models import CloudinaryField


class Table(models.Model):
    table_number = models.IntegerField()
    seats = models.IntegerField()
    
    def __str__(self):
        return f"Table Number {self.table_number}, Seats: {self.seats}"


class Booking(models.Model):
    user = models.ForeignKey(User, related_name='bookings', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    guests = models.IntegerField()
    your_name = models.CharField(max_length=255)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    tables = models.ManyToManyField(Table, through='TableBooking')


class TableBooking(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('table', 'booking')


@transaction.atomic
def create_booking(user, date, time, guests, your_name, email, tables):
    booking = Booking.objects.create(user=user, date=date, time=time, guests=guests, your_name=your_name, email=email)
    for table in tables:
        TableBooking.objects.create(table=table, booking=booking)


class MenuItem(models.Model):
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
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

