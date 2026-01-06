from django.db import models

from django.contrib.auth.models import User


class Profile(models.Model):

    user  = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    phone = models.CharField(max_length=15)

    def __str__(self):

        return self.user.username



class Address(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='addresses')

    full_name = models.CharField(max_length=100)

    phone     = models.CharField(max_length=15)

    house     = models.CharField(max_length=255)

    street    = models.CharField(max_length=255)

    city      = models.CharField(max_length=100)

    state     = models.CharField(max_length=100)

    pincode   = models.CharField(max_length=10)

    def __str__(self):

        return f"{self.full_name} - {self.city}"


