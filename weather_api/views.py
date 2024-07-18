import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .services import get_weather_data


@require_GET
def get_weather(request):
    city = request.GET.get('city')
    if not city:
        return JsonResponse({'error': 'City parameter is required'}, status=400)
    try:
        weather_data = get_weather_data(city)
        return JsonResponse(weather_data)
    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)

