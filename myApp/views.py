from django.views.generic import TemplateView
import requests
from django.shortcuts import render
from environs import Env
from django.core.cache import cache



env = Env()
env.read_env()


class GetWeatherView(TemplateView):
    template_name = 'myApp/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        city = self.request.GET.get('query')
        weather_info = None

        if city:
            weather_info = cache.get(city)

            if not weather_info:
                weather_info = fetch_weather_data(city)
                cache.set(city, weather_info, 300)
                if 'error' not in weather_info and not weather_info.get('current'):
                    weather_info = {'error': "City couldn't be found!"}

        context.update({'weather': weather_info,'city': city})
        return context


def fetch_weather_data(city):
    """Fetch weather data from the API."""
    print("nabooooooooddd")
    api_key = env.str('API_KEY')
    try:
        response = requests.get(
            f'https://api.weatherapi.com/v1/current.json',
            params={'key': api_key, 'q': city}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': f"An error occurred: {str(e)}"}


def receive_coordinates(request):
    current_location_weather = None
    city = None
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    api_key = env.str('API_KEY')

    if lat and lon:
        cache_key = f"weather_{lat}_{lon}"
        print(f"Your cordinates are: lat={lat}, lon={lon}")
        current_location_weather = cache.get(cache_key)

        if not current_location_weather:
            url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={lat},{lon}"
            try:
                response = requests.get(url)
                response.raise_for_status()
                current_location_weather = response.json()
                city = current_location_weather["location"]["name"]
                cache.set(cache_key, current_location_weather, 300)
            except requests.exceptions.RequestException:
                current_location_weather = None

    return render(request, 'myApp/index.html', {'weather': current_location_weather, 'city': city})
