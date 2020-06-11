import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm

def index(request):
    url = 'Enter Your API Key here with the url'
    err_msg = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)
        
        if form.is_valid():
            new_city = form.cleaned_data['name'].capitalize()
            existing_city_count = City.objects.filter(name=new_city).count()

            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'Invalid City '
                    
            else:
                err_msg = 'City Already exists '

        if err_msg:
            message = err_msg
            message_class = 'is_danger'
        else:
            message = 'City Added Successfully'
            message_class = 'is_success'    
                    
    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:
        r = requests.get(url.format(city)).json()
        city_weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['main'],
            'icon' : r['weather'][0]['icon'],
            'country' : r['sys']['country'],
            'coordinates_lon' : r['coord']['lon'],
            'coordinates_lat' : r['coord']['lat'],
            'pressure' : r['main']['pressure'],
            'humidity' : r['main']['humidity']
        }

        print(r)

        weather_data.append(city_weather)

    context = {
        'weather_data' : weather_data, 
        'form' : form,
        'message' : message,
        'message_class' : message_class
    }


    return render(request, 'weather/weather.html', context)

def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    
    return redirect('home')

def delete_everything(request):
    cities = City.objects.all()
    for city in cities:
        City.objects.get(name=city).delete()
    return redirect('home')    
