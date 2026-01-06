# Create your models here.

from django.db import models

import uuid


class BaseClass(models.Model) :

    uuid = models.UUIDField(unique=True,default=uuid.uuid4)

    active_status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta :

        abstract = True



class Category(BaseClass) :

    name = models.CharField(max_length=100)

    class Meta :

        verbose_name = 'Category'

        verbose_name_plural = 'Categories'

    def __str__(self) :

        return f'{self.name}'



class Product(BaseClass):

    name = models.CharField(max_length=200)

    photo = models.ImageField(upload_to='products/photos/',null=True,blank=True)

    description = models.TextField()

    price = models.DecimalField(max_digits=10, decimal_places=2)

    rating = models.DecimalField(max_digits=3, decimal_places=1)

    quantity = models.PositiveIntegerField()

    category = models.CharField(max_length=100)

    brand = models.CharField(max_length=100)

    weight = models.CharField(max_length=50)

    colour = models.CharField(max_length=50)

    sport = models.CharField(max_length=100)

    material = models.CharField(max_length=100)

    class Meta:

        verbose_name = 'Products'

        verbose_name_plural = 'Products'

    def __str__(self):

        return self.name
