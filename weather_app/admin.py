from django.contrib import admin
from .models import WeatherRecord, Location

# Register your models here.
admin.site.register(WeatherRecord)
admin.site.register(Location)