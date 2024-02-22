from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=255) #name of location
    area = models.CharField(max_length=255) #area NSEW of the country

    def __str__(self):
        return f"{self.name}, {self.area}"

class WeatherRecord(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE) #foreign key 
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    daily_rainfall_total = models.FloatField()
    highest_30min_rainfall = models.FloatField()
    highest_60min_rainfall = models.FloatField()
    highest_120min_rainfall = models.FloatField()
    mean_temperature = models.FloatField()
    max_temperature = models.FloatField()
    min_temperature = models.FloatField()
    mean_wind_speed = models.FloatField()
    max_wind_speed = models.FloatField()

    def __str__(self):
        return f"Weather record for {self.location} on {self.date}"
