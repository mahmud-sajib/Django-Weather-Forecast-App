from django.shortcuts import render
from darksky import forecast
from datetime import date, timedelta, datetime

from ipstack import GeoLookup

# Create your views here.

def home(request):

    geo_lookup = GeoLookup("41b1afd1f407de24e54e36d54ceca69c")
    location = geo_lookup.get_own_location()
    lat = location['latitude']
    lng = location['longitude']
    region = location['region_name']
    
    CITY = lat, lng
    
    api_key = '5cd0bb087cf49e0d8503c2dc342f7af1'
    weekday = date.today()

    weekly_weather = {}

    hourly_weather = {}

    with forecast(api_key, *CITY) as city:        
        for day in city.daily:
            day = dict(
            day = date.strftime(weekday, '%a'),
            sum = day.summary,
            tempMin = round((day.temperatureMin-32) * 5.0/9.0),
            tempMax = round((day.temperatureMax-32) * 5.0/9.0) 
            )
            # print('{day}: {sum} Temp range: {tempMin} - {tempMax} C'.format(**day))
            weekday += timedelta(days=1)

            pic = ''
            summary = ('{sum}'.format(**day).lower())

            if 'rain' in summary:
                pic = 'rain.png'
            elif 'cloudy' in summary:
                pic = 'cloudy.png'
            elif 'overcast' in summary:
                pic = 'partly-cloudy.png'
            elif 'clear' in summary:
                pic = 'sunny.png'
            else:
                pic = 'cloudy.png'
            
            weekly_weather.update({
            '{day}'.format(**day):{
                'sum':'{sum}'.format(**day),
                'tempMin':'{tempMin}'.format(**day), 
                'tempMax':'{tempMax}'.format(**day),
                'pic':pic  
            }})

    today = weekly_weather[(date.today().strftime('%a'))]
    del weekly_weather[(date.today().strftime("%a"))]

    
    hour = datetime.now().hour
    location = forecast(api_key, *CITY)
    i = 0

    hour_ = ''

    while hour < 24:

        temp = round((location.hourly[i].temperature-32)* 5.0/9.0)
        

        pic = ''
        summary = location.hourly[i].summary.lower()

        if 'rain' in summary:
            pic = 'rain.png'
        elif 'cloudy' in summary:
            pic = 'cloudy.png'
        elif 'overcast' in summary:
            pic = 'partly-cloudy.png'
        elif 'clear' in summary:
            pic = 'sunny.png'
        else:
            pic = 'cloudy.png'

        if hour < 12:
            hour_ = '{}am'.format(hour)
            hourly_weather.update({hour_:{'pic':pic,'temp':temp}})

        elif hour == 12:
            hour_ = '{}pm'.format(hour)
            hourly_weather.update({hour_:{'pic':pic,'temp':temp}})

        else:
            hour_ = '{}pm'.format(hour-12)
            hourly_weather.update({hour_:{'pic':pic,'temp':temp}})
            
        
        hour += 1
        i += 1


    return render(request, 'index.html', {'weekly_weather':weekly_weather, 'hourly_weather':hourly_weather, 'today':today, 'region':region })
