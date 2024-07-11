import os
import requests
from datetime import datetime
from exceptions import WeatherAPIError

key = os.environ['API_KEY_OPENWEATHER']

WeatherType = {
    'Clouds': 'Облачно',
    'Drizzle': 'Изморось',
    'Thunderstorm': 'Гроза',
    'Rain': 'Дождь',
    'Snow': 'Снег',
    'Clear': 'Ясно',
    'Fog': 'Туман'
}

class Weather:
    def __init__( self, temperature: float,  weather_type: str, sunrise: datetime, sunset: datetime, wind: float, city: str ):
        self.temperature = temperature
        self.weather_type = weather_type
        self.sunrise = sunrise
        self.sunset = sunset
        self.wind = wind
        self.city = city
    def __str__(self):
        return f'В городе {self.city} температура {self.temperature}, ветер {self.wind} м/с, {self.weather_type}'


def get_weather( city: str ) -> Weather:
    try:
        response = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&lang=ru&units=metric&appid={key}")

        data = response.json()

        return Weather(temperature=parse_temperature(data),
                       weather_type=parse_weather_type(data),
                       sunrise=parse_sun_time(data, 'sunrise'),
                       sunset=parse_sun_time(data, 'sunset'),
                       wind=parse_wind(data),
                       city=parse_city(data))
    except:
        raise WeatherAPIError

def parse_temperature( openweather_dict: dict ) -> int:
    return round(openweather_dict["main"]["temp"])

def parse_weather_type ( openweather_dict: dict ) -> str:
    return WeatherType[openweather_dict["weather"][0]["main"]]

def parse_sun_time( openweather_dict: dict,  time: str ) -> datetime:
    return datetime.fromtimestamp(openweather_dict['sys'][time])

def parse_wind( openweather_dict: dict ) -> float:
    return openweather_dict['wind']['speed']

def parse_city( openweather_dict: dict ) -> str:
    return openweather_dict['name']

if __name__ == "__main__":
    print(get_weather('Москва'))
