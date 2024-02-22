from django import forms
from .models import WeatherRecord, Location

class WeatherRecordForm(forms.ModelForm):
    class Meta:
        model = WeatherRecord
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['location'].queryset = Location.objects.all()
