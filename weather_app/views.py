from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse 
from django.http import HttpResponse, HttpResponseRedirect

from .forms import WeatherRecordForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import WeatherRecord, Location
from .serializers import WeatherRecordSerializer

@api_view(['GET', 'POST', 'PUT', 'DELETE'])

#home page index.html
def index(request):
    return render(request, 'index.html')

#about page index.html
def about(request):
    return render(request, 'about.html')

#gets all weather data 
def get_weather_data(request):
    weather_data = WeatherRecord.objects.all()

    #checks if the request wants JSON (API request)
    accept_header = request.META.get('HTTP_ACCEPT', '')
    if 'application/json' in accept_header:
        serializer = WeatherRecordSerializer(weather_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        #this will render html template for non api request
        context = {
            'weather_data': weather_data,
        }
        return render(request, 'all-weather-data.html', context)

#add new weather record into database 
def add_weather_data(request):
    if request.method == 'POST':
        form = WeatherRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all-weather-data')  #this will redirect to the page showing all weather data
    else:
        form = WeatherRecordForm()

    return render(request, 'add-weather-data.html', {'form': form})


#delete exisiting data 
def delete_weather_data(request):
    if request.method == 'GET':
        weather_data = WeatherRecord.objects.all()
        template = loader.get_template('delete-weather-data.html')
        context = {
            'weather_data': weather_data,
        }
        return render(request, 'delete-weather-data.html', context)

    elif request.method == 'POST':
        record_id = request.POST.get('record_id')
        try:
            record = WeatherRecord.objects.get(pk=record_id)
            record.delete()
        except WeatherRecord.DoesNotExist:
            pass  #for when the record does not exist

        return HttpResponseRedirect(reverse('delete-weather-data'))

@api_view(['GET', 'DELETE'])
def delete_weather_record(request, pk):
    try:
        record = WeatherRecord.objects.get(pk=pk)
    except WeatherRecord.DoesNotExist:
        return Response({'error': 'Weather record not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = WeatherRecordSerializer(record)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        record.delete()
        return Response({'success': 'Weather record deleted'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
#update existing weather data page 
def update_weather_data(request):
    weather_data = WeatherRecord.objects.all()
    template = 'update-weather-data.html'
    context = {
        'weather_data': weather_data,
    }
    return render(request, template, context)

#updating specific weather data 
def update_weather_record(request, pk):
    data_update = get_object_or_404(WeatherRecord, pk=pk)
    template = 'update-weather-data.html'  
    context = {
        'data_update': data_update,
    }
    return render(request, template, context)

@api_view(['POST'])
#updating specific weather data for each column of data 
def update_weather_detail(request, pk):
    if request.method == 'POST':
        location_name = request.POST.get('location')
        year = request.POST.get('year')
        month = request.POST.get('month')
        day = request.POST.get('day')
        daily_rainfall_total = request.POST.get('daily_rainfall_total')
        highest_30min_rainfall = request.POST.get('highest_30min_rainfall')
        highest_60min_rainfall = request.POST.get('highest_60min_rainfall')
        highest_120min_rainfall = request.POST.get('highest_120min_rainfall')
        mean_temperature = request.POST.get('mean_temperature')
        max_temperature = request.POST.get('max_temperature')
        min_temperature = request.POST.get('min_temperature')
        mean_wind_speed = request.POST.get('mean_wind_speed')
        max_wind_speed = request.POST.get('max_wind_speed')

        location, created = Location.objects.get_or_create(name=location_name)

        #update the record below
        weather_record = get_object_or_404(WeatherRecord, pk=pk)
        weather_record.location = location
        weather_record.year = year
        weather_record.month = month
        weather_record.day = day
        weather_record.daily_rainfall_total = daily_rainfall_total
        weather_record.highest_30min_rainfall = highest_30min_rainfall
        weather_record.highest_60min_rainfall = highest_60min_rainfall
        weather_record.highest_120min_rainfall = highest_120min_rainfall
        weather_record.mean_temperature = mean_temperature
        weather_record.max_temperature = max_temperature
        weather_record.min_temperature = min_temperature
        weather_record.mean_wind_speed = mean_wind_speed
        weather_record.max_wind_speed = max_wind_speed
        
        weather_record.save() #saves the updated record here

        return HttpResponseRedirect(reverse('update-weather-data'))

    data_update = get_object_or_404(WeatherRecord, pk=pk)
    template = 'update-weather-detail.html'  
    context = {
        'data_update': data_update,
    }
    return render(request, template, context)

#gets all weather record by date 
def get_weather_record_by_date(request):
    if request.method == 'POST':
        #extracts date values from the form
        year = request.POST.get('year')
        month = request.POST.get('month')
        day = request.POST.get('day')

        #query the database for weather records matching the specified date
        weather_records = WeatherRecord.objects.filter(year=year, month=month, day=day)

        #pass the weather records to the template for display
        context = {
            'weather_records': weather_records,
            'selected_date': f'{year}-{month}-{day}',
        }
        return render(request, 'weather-record-by-date.html', context)

    return render(request, 'get-weather-by-date.html')

#gets all weather record by location 
def get_weather_record_by_location(request):
    if request.method == 'POST':
        #extracts location value from the form
        location_id = request.POST.get('location')

        #query the database for weather records matching the specified location ID
        weather_records = WeatherRecord.objects.filter(location_id=location_id)
        location_name = get_object_or_404(Location, id=location_id).name

        #pass the weather records to the template for display
        context = {
            'weather_records': weather_records,
            'location_name' : location_name
        }
        return render(request, 'weather-record-by-location.html', context)

    #pass the available locations to the template
    locations = Location.objects.all()
    return render(request, 'get-weather-by-location.html', {'locations': locations})


#gets the date most extreme weather (rain + max temp + max wind) for a specific location 
def get_extreme_weather_by_location(request):
    if request.method == 'POST':
        #extracts location value from the form
        location_id = request.POST.get('location')

        #query the database for weather records matching the specified location
        weather_records = WeatherRecord.objects.filter(location__id=location_id)

        #find the record with the highest values for rainfall, max temperature, and max wind speed
        extreme_weather_record = weather_records.order_by(
            '-daily_rainfall_total', '-max_temperature', '-max_wind_speed'
        ).first()

        if extreme_weather_record:
            context = {
                'location': extreme_weather_record.location,
                'date': f"{extreme_weather_record.year}-{extreme_weather_record.month}-{extreme_weather_record.day}",
                'weather_data': extreme_weather_record,
            }
            return render(request, 'extreme-weather-data.html', context)

    locations = Location.objects.all()
    return render(request, 'get-extreme-weather.html', {'locations': locations})

