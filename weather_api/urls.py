from django.urls import path

from weather_api.views import get_weather

urlpatterns = [
    path('weather/', get_weather, name='weather'),
]