from django.test import TestCase, Client
from unittest.mock import patch
from django.urls import reverse
import requests


class WeatherViewTests(TestCase):

    @patch('weather_api.services.get_weather_data')
    def test_get_weather_success(self, mock_get_weather_data):

        mock_get_weather_data.return_value = {
            "location": {
                "name": "Paris",
                "region": "Ile-de-France",
                "country": "France",
                "lat": 48.87,
                "lon": 2.33,
                "tz_id": "Europe/Paris",
                "localtime_epoch": 1721215151,
                "localtime": "2024-07-17 13:19"
            },
            "current": {
                "last_updated_epoch": 1721214900,
                "last_updated": "2024-07-17 13:15",
                "temp_c": 25.4,
                "temp_f": 77.7,
                "is_day": 1,
                "condition": {
                    "text": "Partly Cloudy",
                    "icon": "//cdn.weatherapi.com/weather/64x64/day/116.png",
                    "code": 1003
                },
                "wind_mph": 2.2,
                "wind_kph": 3.6,
                "wind_degree": 210,
                "wind_dir": "SSW",
                "pressure_mb": 1021,
                "pressure_in": 30.15,
                "precip_mm": 0,
                "precip_in": 0,
                "humidity": 41,
                "cloud": 33,
                "feelslike_c": 25.7,
                "feelslike_f": 78.2,
                "windchill_c": 25.4,
                "windchill_f": 77.7,
                "heatindex_c": 25.7,
                "heatindex_f": 78.2,
                "dewpoint_c": 11.1,
                "dewpoint_f": 51.9,
                "vis_km": 10,
                "vis_miles": 6,
                "uv": 7,
                "gust_mph": 6.7,
                "gust_kph": 10.8
            }
        }

        client = Client()
        response = client.get(reverse('weather') + '?city=Paris')

        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertIn("location", response_data)
        self.assertIn("name", response_data["location"])
        self.assertIn("region", response_data["location"])
        self.assertIn("country", response_data["location"])
        self.assertIn("lat", response_data["location"])
        self.assertIn("lon", response_data["location"])

        self.assertEqual(response_data["location"]["name"], "Paris")
        self.assertEqual(response_data["location"]["region"], "Ile-de-France")
        self.assertEqual(response_data["location"]["country"], "France")
        self.assertEqual(response_data["location"]["lat"], 48.87)
        self.assertEqual(response_data["location"]["lon"], 2.33)

    def test_get_weather_no_city(self):
        client = Client()
        response = client.get(reverse('weather'))
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content.decode('utf-8'), {'error': 'City parameter is required'})

    @patch('weather_api.services.get_weather_data')
    def test_get_weather_api_error(self, mock_get_weather_data):

        mock_get_weather_data.side_effect = requests.RequestException("API error")
        client = Client()
        response = client.get(reverse('weather') + '?city=InvalidCity')
        self.assertEqual(response.status_code, 500)
        self.assertJSONEqual(response.content.decode('utf-8'), {
            'error': '400 Client Error: Bad Request for url: https://api.weatherapi.com/v1/current.json?key=0d52723c0cae42588c3102455241707&q=InvalidCity'
        })
