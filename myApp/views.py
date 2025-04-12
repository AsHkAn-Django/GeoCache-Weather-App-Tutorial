from django.views.generic import TemplateView
import requests
from django.shortcuts import render
from environs import Env


env = Env()
env.read_env()


class GetWeatherView(TemplateView):
    template_name = 'myApp/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        city = self.request.GET.get('query')
        weather_info = None
        
        if city:
            weather_info = fetch_weather_data(city)
            if 'error' not in weather_info and not weather_info.get('current'):
                weather_info = {'error': "City couldn't be found!"}
                        
        context.update({'weather': weather_info,'city': city})
        return context


def fetch_weather_data(city):
    """Fetch weather data from the API."""
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
    """Show the user's current location weather."""
    coords = request.GET.getlist("coord") 
    api_key = env.str('API_KEY')

    if coords:
        lat = coords[0]
        lon = coords[1]
        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={lat},{lon}"
        try:
            response = response = requests.get(url)
            response.raise_for_status()
            current_location = response.json()
            city = current_location["location"]["name"]
        except requests.exceptions.RequestException:
            current_location = None
            city = None    
    return render(request, 'myApp/index.html', {'weather':current_location, 'city': city})