# from django.core.files import File
# from io import BytesIO
# import PIL
from random import choices
# TODO: models coming to gis
from django.contrib.gis.db import models
from django.utils import timezone
from django.contrib.gis.geos import Point
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


class User(AbstractUser):
    firstname = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True)
    lon = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    lat = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    location = models.PointField(srid=4326, blank=True, null=True)
    
    USERNAME_FIELD = "email"
    # requred for creating user
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def get_full_name(self):
        return self.firstname + self.lastname


# this can be a profile for example
class Location(models.Model):
    point = models.PointField(srid=4326, blank=True, null=True)