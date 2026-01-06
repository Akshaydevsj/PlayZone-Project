from django.db import models

import uuid

from django.contrib.auth.models import User

from multiselectfield import MultiSelectField



class BaseClass(models.Model):

    uuid = models.UUIDField(unique=True, default=uuid.uuid4)

    active_status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        abstract = True



class GroundTypeChoices(models.TextChoices):

    MUD = 'Mud', 'Mud'

    GRASS = 'Grass', 'Grass'

    ARTIFICIAL = 'Artificial Grass', 'Artificial Grass'

    WOODEN = 'Wooden Floor', 'Wooden Floor'

    SYNTHETIC = 'Synthetic Floor', 'Synthetic Floor'



class BookingStatusChoices(models.TextChoices):

    CONFIRMED = 'Confirmed', 'Confirmed'

    COMPLETED = 'Completed', 'Completed'

    CANCELLED = 'Cancelled', 'Cancelled'

    

class TurfOwner(BaseClass):

    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='turf_owner')

    owner_name = models.CharField(max_length=100)

    email = models.EmailField()

    phone = models.CharField(max_length=15)

    account_holder_name = models.CharField(max_length=100)

    account_number = models.CharField(max_length=20)

    ifsc_code = models.CharField(max_length=15)

    pan_number = models.CharField(max_length=15)

    class Meta:

        verbose_name = 'Turf Owner'

        verbose_name_plural = 'Turf Owners'

    def __str__(self):

        return f'{self.owner_name}'




class Turf(BaseClass):

    owner = models.ForeignKey(TurfOwner,on_delete=models.CASCADE,related_name='turfs')

    turf_name = models.CharField(max_length=100, unique=True)

    turf_image = models.ImageField(upload_to='turfs/images')

    city = models.CharField(max_length=100)

    address = models.TextField()

    landmark = models.CharField(max_length=150)

    google_map_link = models.URLField()

    games = models.CharField(max_length=255,help_text="Enter games separated by comma (e.g., Football, Cricket)")

    ground_type = models.CharField(max_length=30,choices=GroundTypeChoices.choices)

    price_per_hour = models.PositiveIntegerField()

    light_extra_charge = models.PositiveIntegerField(default=200)

    is_approved = models.BooleanField(default=False)

    is_booking_open = models.BooleanField(default=True)

    is_denied = models.BooleanField(default=False)
    
    admin_delete_reason = models.TextField(blank=True, null=True)


    class Meta:

        verbose_name = 'Turf'

        verbose_name_plural = 'Turfs'

    def __str__(self):

        return f'{self.turf_name}'



class TurfBooking(BaseClass):

    turf = models.ForeignKey(Turf,on_delete=models.CASCADE,related_name='bookings')

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='turf_bookings')

    customer_name = models.CharField(max_length=100)

    customer_phone = models.CharField(max_length=15)

    booking_date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    total_hours = models.PositiveIntegerField()

    base_amount = models.PositiveIntegerField()

    light_charge = models.PositiveIntegerField()

    total_amount = models.PositiveIntegerField()

    payment_done = models.BooleanField(default=False)

    status = models.CharField(max_length=20,choices=BookingStatusChoices.choices,default=BookingStatusChoices.CONFIRMED)

    class Meta:

        verbose_name = 'Turf Booking'

        verbose_name_plural = 'Turf Bookings'

    def __str__(self):

        return f'{self.turf.turf_name} | {self.booking_date}'

