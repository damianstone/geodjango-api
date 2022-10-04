from django.contrib.gis import admin
from django.contrib.auth.admin import UserAdmin
from .models import Location, User

# TODO: add OSMGeoAdmin
admin.site.register(User, admin.OSMGeoAdmin)
admin.site.register(Location, admin.OSMGeoAdmin)

