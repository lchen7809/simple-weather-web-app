#load and store python script
import os
import sys

current_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.join(current_path, "..")
sys.path.append(parent_path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weather_project.settings")

import django
django.setup()

import csv
from weather_app.models import Location, WeatherRecord
from datetime import datetime

def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            location, created = Location.objects.get_or_create(
                name=row['Station'],
                area=row['Area']
            )
            location.save()

            weather_record = WeatherRecord(
                location=location,
                year=row['Year'],
                month=row['Month'],
                day=row['Day'],
                daily_rainfall_total=row['Daily Rainfall Total (mm)'],
                highest_30min_rainfall=row['Highest 30 min Rainfall (mm)'],
                highest_60min_rainfall=row['Highest 60 min Rainfall (mm)'],
                highest_120min_rainfall=row['Highest 120 min Rainfall (mm)'],
                mean_temperature=row['Mean Temperature (°C)'],
                max_temperature=row['Maximum Temperature (°C)'],
                min_temperature=row['Minimum Temperature (°C)'],
                mean_wind_speed=row['Mean Wind Speed (km/h)'],
                max_wind_speed=row['Max Wind Speed (km/h)']
            )
            weather_record.save()
            
if __name__ == "__main__":
    load_data('csv/area_cleaned_data.csv')
