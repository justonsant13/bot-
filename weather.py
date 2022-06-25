import json
import requests as req
import telebot
from geopy import geocoders
from os import environ

appid = "0de4a2b2-b300-4b85-8ef9-aa78e4769bb2"
token = '5505212365:AAFY2yZLiFyHnDxNvqOOupmaFGM5VxTBevg'
def print_yandex_weather(dict_weather_yandex, message, bot):
    day = {'night': 'ночью', 'morning': 'утром', 'day': 'днем', 'evening': 'вечером', 'fact': 'сейчас'}
    bot.send_message(message.from_user.id, f'А яндекс говорит:')
    bot.send_message('А яндекс говорит:')
    for i in dict_weather_yandex.keys():
        if i != 'link':
            time_day = day[i]
            bot.send_message(message.from_user.id, f'Температура {time_day} {dict_weather_yandex[i]["temp"]}'
                                                   f', на небе {dict_weather_yandex[i]["condition"]}')

    bot.send_message(message.from_user.id, f' А здесь ссылка на подробности 'f'{dict_weather_yandex["link"]}')

    bot = telebot.TeleBot(token)
    bot.polling(none_stop=True)

def geo_pos(city: str):
        geolocator = geocoders.Nominatim(user_agent="telebot")
        latitude = str(geolocator.geocode(city).latitude)
        longitude = str(geolocator.geocode(city).longitude)
        return latitude, longitude
def yandex(latitude, longitude, token_yandex: str):
    url_yandex = f'https://api.weather.yandex.ru/v2/forecast/?lat={latitude}&lon={longitude}&[lang=ru_RU]'
    yandex_req = req.get(url_yandex, headers={'X-Yandex-API-Key': token_yandex}, verify=False)
    yandex_json = json.loads(yandex_req.text)
    con = yandex_json['fact']['condition']
    return yandex_json
conditions = {'clear': 'ясно', 'partly-cloudy': 'малооблачно', 'cloudy': 'облачно с прояснениями',
                  'overcast': 'пасмурно', 'drizzle': 'морось', 'light-rain': 'небольшой дождь',
                  'rain': 'дождь', 'moderate-rain': 'умеренно сильный', 'heavy-rain': 'сильный дождь',
                  'continuous-heavy-rain': 'длительный сильный дождь', 'showers': 'ливень',
                  'wet-snow': 'дождь со снегом', 'light-snow': 'небольшой снег', 'snow': 'снег',
                  'snow-showers': 'снегопад', 'hail': 'град', 'thunderstorm': 'гроза',
                  'thunderstorm-with-rain': 'дождь с грозой', 'thunderstorm-with-hail': 'гроза с градом'
                  }
c=geo_pos('Москва')
lat=c[0]
lon=c[1]
print(geo_pos('Екатеринбург'))
print(lat)
print(lon)
w=yandex(c[0],c[1],appid)
con= conditions[w['fact']['condition']]
print(con)


def yandex_weather_fact(latitude, longitude, token_yandex: str):
    url_yandex = f'https://api.weather.yandex.ru/v2/forecast/?lat={latitude}&lon={longitude}&[lang=ru_RU]'
    yandex_req = req.get(url_yandex, headers={'X-Yandex-API-Key': token_yandex}, verify=False)
    conditions = {'clear': 'ясно', 'partly-cloudy': 'малооблачно', 'cloudy': 'облачно с прояснениями',
                  'overcast': 'пасмурно', 'drizzle': 'морось', 'light-rain': 'небольшой дождь',
                  'rain': 'дождь', 'moderate-rain': 'умеренно сильный', 'heavy-rain': 'сильный дождь',
                  'continuous-heavy-rain': 'длительный сильный дождь', 'showers': 'ливень',
                  'wet-snow': 'дождь со снегом', 'light-snow': 'небольшой снег', 'snow': 'снег',
                  'snow-showers': 'снегопад', 'hail': 'град', 'thunderstorm': 'гроза',
                  'thunderstorm-with-rain': 'дождь с грозой', 'thunderstorm-with-hail': 'гроза с градом'
                  }
    wind_dir = {'nw': 'северо-западное', 'n': 'северное', 'ne': 'северо-восточное', 'e': 'восточное',
                'se': 'юго-восточное', 's': 'южное', 'sw': 'юго-западное', 'w': 'западное', 'с': 'штиль'}
    pressure_mm = {'clear'}
    humidity = {'clear'}
    temp_avg = {'clear'}
    temp = {'clear'}
    yandex_json = json.loads(yandex_req.text)
    pogoda = dict()
    yandex_json['fact']['condition'] = conditions[yandex_json['fact']['condition']]
    yandex_json['fact']['wind_dir'] = wind_dir[yandex_json['fact']['wind_dir']]

    # pogoda['humidity'] = yandex_json['forecasts'][0]['parts']['day']['humidity']
    pogoda['humidity'] = yandex_json['fact']['humidity']
    pogoda['feels_like'] = yandex_json['fact']['feels_like']
    pogoda['temp'] = yandex_json['fact']['temp']
    pogoda['condition'] = yandex_json['fact']['condition']
    pogoda['wind_dir'] = yandex_json['fact']['wind_dir']
    pogoda['pressure_mm'] = yandex_json['fact']['pressure_mm']
    params = ['condition', 'wind_dir', 'pressure_mm', 'humidity', 'temp_avg' 'temp']

    return pogoda
