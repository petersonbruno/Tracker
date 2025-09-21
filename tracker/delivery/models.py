from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('shop_owner', 'Shop Owner'),
        ('driver', 'Driver'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    groups = models.ManyToManyField(
        Group,
        related_name='delivery_user_set',  # avoid clash with auth.User.groups
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='delivery_user_set',  # avoid clash with auth.User.user_permissions
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )



class House(models.Model):
    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    area_name = models.CharField(max_length=100)
    postcode = models.CharField(max_length=20)
    landmark = models.TextField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.customer_name} - {self.postcode}"


class Delivery(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=100)
    package_details = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('on_the_way', 'On the Way'), ('delivered', 'Delivered')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
