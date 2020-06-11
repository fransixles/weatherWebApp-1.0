from django.forms import ModelForm, TextInput
from .models import City

class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {'name' : TextInput(attrs={'class' : 'input is-success is-focused is-outlined is-rounded', 'placeholder' : 'Enter City Name'})}
