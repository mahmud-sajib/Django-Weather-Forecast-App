from django.shortcuts import render
from darksky import forecast
from datetime import date, timedelta, datetime

# Create your views here.

def home(request):
    DHAKA = 23.7104, 90.4074
    #units='si'
    api_key = '5cd0bb087cf49e0d8503c2dc342f7af1'
    weekday = date.today()

    with forecast(api_key, *DHAKA) as dhaka:        
        for day in dhaka.daily:
            day = dict(day = date.strftime(weekday, '%a'),
            sum = day.summary,
            tempMin = round((day.temperatureMin-32) * 5.0/9.0),
            tempMax = round((day.temperatureMax-32) * 5.0/9.0) 
            )
            print('{day}: {sum} Temp range: {tempMin} - {tempMax} C'.format(**day))
            weekday += timedelta(days=1)
    
    hour = datetime.now().hour
    location = forecast(api_key, *DHAKA)
    i = 0

    while hour < 24:
        temp = location.hourly[i].temperature

        if hour < 12:
            print('{}am -- {}temp'.format(hour,temp))
        else:
            print('{}pm -- {}temp'.format(hour,temp))
        
        hour += 1
        i += 1

    return render(request,'index.html')
