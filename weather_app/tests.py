from django.test import TestCase
from django.urls import reverse
from .models import Location, WeatherRecord

class WeatherAppTests(TestCase):

    def setUp(self):
        #creating a location for testing
        self.location = Location.objects.create(name='Test Location', area='Test Area')

        #creating a weather record for testing
        self.weather_record = WeatherRecord.objects.create(
            location=self.location,
            year=2023,
            month=1,
            day=1,
            daily_rainfall_total=10.5,
            highest_30min_rainfall=5.5,
            highest_60min_rainfall=7.5,
            highest_120min_rainfall=8.5,
            mean_temperature=25.0,
            max_temperature=30.0,
            min_temperature=20.0,
            mean_wind_speed=15.0,
            max_wind_speed=20.0,
        )

    def test_get_weather_record_by_location(self):

        response = self.client.post(reverse('get-weather-record-by-location'), {'location': self.location.id})

        #if success response status code 200
        self.assertEqual(response.status_code, 200)

        #checks if the location name is present
        self.assertIn('location_name', response.context)

        #checks if the weather records for the location are present
        self.assertIn('weather_records', response.context)

        #checks if the correct location name is displayed in the rendered html
        self.assertContains(response, self.location.name)

        #checks if the correct weather record date information is present in the rendered html
        self.assertContains(response, str(self.weather_record.year))
        self.assertContains(response, str(self.weather_record.month))
        self.assertContains(response, str(self.weather_record.day))
        #some additional checks of information is present
        self.assertContains(response, str(self.weather_record.daily_rainfall_total))
        self.assertContains(response, str(self.weather_record.mean_temperature))

        #checks if specific data is not present in the HTML
        self.assertNotContains(response, 'This should not be present')

