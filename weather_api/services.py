import requests


def get_weather_data(city):
    api_key = '0d52723c0cae42588c3102455241707'  # Remplacez par votre clé API WeatherAPI
    url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
