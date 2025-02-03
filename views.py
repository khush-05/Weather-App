from django.shortcuts import render
import requests
from datetime import datetime, timedelta
from django.utils.timezone import now


# Function to convert UTC timestamp to IST
def convert_to_ist(utc_timestamp):
    utc_time = datetime.fromtimestamp(utc_timestamp)  
    ist_time = utc_time + timedelta(hours=5, minutes=30)  
    return ist_time.strftime('%H:%M %p')  


def Weather_app(request):
    city = request.GET.get('city', 'Pune')  
    api = "ffca7fa49270a4896d0bf28218d62005"
    
    
    curr_weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}'
    daily_weather_url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api}'
    
    
    data1 = requests.get(curr_weather_url).json()
    data2 = requests.get(daily_weather_url).json()
    
    
    current_time = now()
    
    
    payload1 = {
        'city': data1['name'],
        'weather': data1['weather'][0]['main'],
        'icon': data1['weather'][0]['icon'],
        'temprature': int(data1['main']['temp'] - 273),  # Convert from Kelvin to Celsius
        'pressure': data1['main']['pressure'],
        'humidity': data1['main']['humidity'],
        'feelslike': int(data1['main']["feels_like"] - 273),
        'mintemp': int(data1['main']["temp_min"] - 273),
        'maxtemp': int(data1['main']["temp_max"] - 273),
        'sunrise': convert_to_ist(data1['sys']['sunrise']),
        'sunset': convert_to_ist(data1['sys']['sunset']),
        'date': current_time.strftime('%d-%B-%Y'),
        'time': (current_time + timedelta(hours=5, minutes=30)).strftime('%I:%M %p'),  
        'day': current_time.strftime('%A')
    }

    
    forecast = []
    seen_dates = set()
    for entry in data2['list']:
        date = entry['dt_txt'].split()[0]  
        day_obj = datetime.strptime(date, '%Y-%m-%d')
        day = day_obj.strftime('%A')
        forecast_ist_time = datetime.strptime(entry['dt_txt'], '%Y-%m-%d %H:%M:%S') + timedelta(hours=5, minutes=30)  
        
        if date not in seen_dates:  
            seen_dates.add(date)
            forecast.append({
                'Day': day,
                'date': forecast_ist_time.strftime('%d-%B-%Y %I:%M %p'),
                'weather': entry['weather'][0]['main'],
                'icon': entry['weather'][0]['icon'],
                'temperature': int(entry['main']['temp'] - 273),
                'pressure': entry['main']['pressure'],
                'humidity': entry['main']['humidity']
            })
        
        if len(forecast) == 5:  # Limit to 5 days
            break

    
    context = {
        'Curr_weather': payload1,
        'forecast': forecast
    }
    
    
    return render(request, 'Weather.html', context)
