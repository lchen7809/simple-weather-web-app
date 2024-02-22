from django.urls import path
# from .import views 
from .views import (
    index,
    about,
    get_weather_data,
    add_weather_data,
    delete_weather_data,
    delete_weather_record,
    update_weather_data,
    update_weather_record,
    update_weather_detail,
    get_weather_record_by_date,
    get_weather_record_by_location,
    get_extreme_weather_by_location
    )

urlpatterns = [
    path('', index, name='index'),
    path('about', about, name='about'),
    path('api/all_weather_data/', get_weather_data, name='all-weather-data'),
    path('api/add_weather_data/', add_weather_data, name='add-weather-data'),
    path('api/delete_weather_data/', delete_weather_data, name='delete-weather-data'),
    path('api/delete_weather_record/<int:pk>/', delete_weather_record, name='delete-weather-record'),
    path('api/update_weather_data/', update_weather_data, name='update-weather-data'),
    path('api/update_weather_record/<int:pk>/', update_weather_record, name='update-weather-record'),
    path('api/update_weather_detail/<int:pk>/', update_weather_detail, name='update-weather-detail'),
    path('api/get_weather_record_by_date/', get_weather_record_by_date, name='get-weather-record-by-date'),
    path('api/get_weather_record_by_location/', get_weather_record_by_location, name='get-weather-record-by-location'),
    path('api/get_extreme_weather/', get_extreme_weather_by_location, name='get-extreme-weather'),

]

