# script will be scheduled to run every morning at 8:00 

import json
import requests
from pprint import pprint
import time 
import datetime as dt
from random import choice
import yagmail 

with open('apikey.json') as f:
    # api key from https://openweathermap.org/
    api_key = json.load(f)['weather_api'] 

# api call
city = 'Prague'
units = 'metric'
url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units={units}'
r = requests.get(url)
content = r.json()

# initalization of variables holding time throughout the day
daytime = [now := content['list'][0],noon := content['list'][1], afternoon := content['list'][2], 
       evening := content['list'][3], night := content['list'][4]]

# pressure
def get_pressure() -> list:
    pressure = []
    for hour in daytime:
        pressure.append(hour['main']['grnd_level'])
    return pressure

def classify_pressure(pressure : list) -> str:
    if sum(pressure)/len(pressure) < 990:
        return 'pretty low, so don\'t forget to drink enough water and eat nutritious food.' 
    elif min(pressure) < 1000 or sum(pressure)/len(pressure) >= 990 and sum(pressure)/len(pressure) <= 1000:
        return 'low, so it might make you feel tired during the day. To be prepared have something sweet on you (;'
    elif sum(pressure)/len(pressure) > 1000 and sum(pressure)/len(pressure) <= 1020:
        return 'normal so you should be feeling well (hope you slept well).'
    elif min(pressure) >= 1020:
        return 'really high so watch out for any head or muscle pain and drink enough water.'
    elif sum(pressure)/len(pressure) >= 1020 or max(pressure) >= 1020:
        return 'pretty high but don\'t worry. Just drink enough water and you should be fine.'

# temperature
def find_min_temp(daytime : list) -> float:
    minimum = float(now['main']['temp_min'])
    for hour in daytime:
        if float(hour['main']['temp_min']) < minimum:
            minimum = float(hour['main']['temp_min'])
    return minimum

def find_max_temp(day : list) -> float:
    maximum = float(now['main']['temp_max'])
    for hour in day:
        if float(hour['main']['temp_max']) > maximum:
            maximum = float(hour['main']['temp_max'])
    return maximum

def temp_data(data : dict) -> dict:
    return {'temp' : data['main']['temp'], 'feels' : data['main']['feels_like']}

def temp_message() -> str:
    high = find_max_temp(daytime)
    low = find_min_temp(daytime)
    if low <= -6:
        return 'today\'s weather will be no joke so a warm tea or coffee will surely help'
    elif high <= 0:
        return 'be prepared for a cold day and wear warm socks'
    elif high > 0 and high <= 6 and low <= 0:
        return 'we are of to a cold day. Be prepared for that'
    elif high > 0 and low <= 6:
        return 'do not forget your jacket today'
    elif high > 6 and high < 10 and low > 6:
        return 'pretty breezy day ahead'
    elif high >=12 and low >= 12:
        return 'breezy weather, definitely wear a hoodie but you shouldn\'t be too cold'
    elif low >= 10 and low <= 17:
        return 'it could be nice but we\'d recommend to leave the shorts at home at least for the morning'
    elif low > 17 and low < 25:
        return 'should be pretty warm day, hope you make the best of it'
    elif high >= 25 and low >= 18 and high <= 30:
        return 'warm day it is, shouldn\'t be too hot so wear something comfortable and enjoy'
    elif low >= 25 and low < 29:
        return 'degrees are up and hopefully your mood as well'
    elif low >= 29:
        return 'beware a really tropical day have something to drink, today will be hot'
    else:
        return 'temperature will be really something today, be prepared and have fun'
    
# sunrise & sunset
def extract_sun_data() -> dict:
    # sunset time formatted to suitable output
    sunrise_time = time.ctime(int(content['city']['sunrise'])).split(' ')[-2][:-3] 
    
    # sunrise time formatted to suitable output
    sunset_time = time.ctime(int(content['city']['sunset'])).split(' ')[-2][:-3]
    return {'sunrise' : sunrise_time,
            'sunset' : sunset_time}

# wind
def extract_wind() -> str:
    wind_list = [daytime[i]['wind']['speed'] for i in range(len(daytime))]
    if max(wind_list) < 3:
        return f'No need to worry about wind today as it will not be surpass the speed of {max(wind_list)}m/s.'
    elif max(wind_list) < 5:
        return 'When it comes to wind we aren\'t expecting anything stronger than a breeze.'    
    elif max(wind_list) < 10:
        return f'Today we are expecting a gentle breeze with the speed up to {max(wind_list)}m/s.'
    elif max(wind_list) < 14:
        return f'The wind today should rise up to {max(wind_list)}m/s so be prepared for a bit of wind.'
    elif max(wind_list) < 20:
        return f'Today we are expecting really strong wind with peaking at {max(wind_list)}m/s. Which can even complicate walking.'
    else:
        return f'Be prepared for extremely strong wind with a speed of {max(wind_list)}m/s. Which can break tree branches or cause other damage.'

wish = ['hope you have a beautiful day.', 'are you ready for new day?', 'hope you are having a great start to the new day', 
        'let\'s see what is out there.', 'let\'s read a morning report shall we?']

if __name__ == '__main__':
    
    # list holding sunrise and sunset
    sun = extract_sun_data()
    was_were = 'was' if sun['sunrise'] < '08:00' else 'will be'
    
    # date in dd.mm.yyyy format
    date = str(dt.datetime.now()).split(' ')[0]
    date = '.'.join(list(date.split('-'))[::-1])
    
    # string of the day in week (eg. Tuesday)
    day = dt.datetime.now().strftime("%A")

    pressure = get_pressure()

    weather = daytime[0]['weather'][0]['description']
    is_are = 'are' if weather[-1] == 's' else 'is'
    
    # messages for rainy weather
    umbrella_message = ' so have your umbrella ready.' if 'rain' in weather else '.'
    second_umbrella_message = ' But have an umbrella with you as there\'s expected rain later in the day.' if 'rain' in ''.join(weather) else ''
    storm_warning = ' Also be careful today as there\'s forecasted a storm today.' if 'storm' in ''.join(weather) else ''
    rain_summary = ' No significant rain or storm is forecasted the day.' if umbrella_message == '.' and second_umbrella_message == '' and storm_warning == '' else ''
    
    # content for email
    text = f"""\
            Hi,        
    
            it's {day} ({date}) {choice(wish)} Today\'s sunrise {was_were} at {sun['sunrise']} 
            and sun will set at {sun['sunset']}. Currently there\'s {temp_data(now)['temp']}°C outside and it 
            feels like {temp_data(now)['feels']}°C. Today's temperature should stay inbetween {find_min_temp(daytime)}°C and {find_max_temp(daytime)}°C so 
            {temp_message()}. {extract_wind()}
    
            There {is_are} currently {weather} outside{umbrella_message}{second_umbrella_message}{storm_warning}{rain_summary} Finally we 
            are expecting a pressure around {sum(pressure)/len(pressure)}hPa which is considered 
            {classify_pressure(pressure)}
            
            We wish you well and hope you have a smashing day today.
            """
    # sending an email
    with open('mail.json') as f:
        # mail sender + pass and reciever
        data = json.load(f) 
    
    sender = data.get("sender")         # sender doesn't include @gmail.com domain
    passwd = data.get("pass")
    reciever = data.get("reciever")     # may be altered to list in order to send multiple emails
    
    yag = yagmail.SMTP(user=sender, password=passwd)
    yag.send(to=reciever, subject='Morning report', contents=text)