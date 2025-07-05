from django.views.generic import TemplateView
import requests
from django.shortcuts import render
from django.core.cache import cache
from django.conf import settings
import logging


logger = logging.getLogger(__name__)

API_KEY = settings.WEATHERAPI_API_KEY


class GetWeatherView(TemplateView):
    """If there is a city is return the current weather for it."""
    template_name = 'myApp/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        city = self.request.GET.get('query')
        weather_info = None

        if city:
            weather_info = cache.get(city)
            if not weather_info:
                weather_info = fetch_weather_for_city(city)
                cache.set(city, weather_info, 300)
                if 'error' not in weather_info and not weather_info.get('current'):
                    weather_info = {'error': "City couldn't be found!"}

        context.update({'weather': weather_info,'city': city})
        return context


def fetch_weather_for_city(city):
    """Fetch weather data from the API for an specific city."""
    try:
        response = requests.get(
            f'https://api.weatherapi.com/v1/current.json',
            params={'key': API_KEY, 'q': city}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': f"An error occurred: {str(e)}"}


def receive_coordinates(request):
    """Get the coordinates of current location of user."""
    current_location_weather = None
    city = None
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')

    if lat and lon:
        cache_key = f"weather_{lat}_{lon}"
        logger.info(f"✅ Geolocation got the Coordinates Successfuly! Your coordinates are: lat={lat}, lon={lon}")

        current_location_weather = cache.get(cache_key)

        if not current_location_weather:
            weather_data = fetch_weather_for_cord(lat, lon, cache_key)
            if weather_data and "location" in weather_data:
                city = weather_data["location"]["name"]
                current_location_weather = weather_data
        else:
            if "location" in current_location_weather:
                city = current_location_weather["location"]["name"]

    return render(request, 'myApp/index.html', {'weather': current_location_weather, 'city': city})




def fetch_weather_for_cord(lat, lon, cache_key):
    """Gets lat, lon, and cache_key and bring back the weather."""
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={lat},{lon}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        current_location_weather = response.json()
        cache.set(cache_key, current_location_weather, 300)
        return current_location_weather
    except requests.exceptions.RequestException:
        current_location_weather = None