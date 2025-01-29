from django.views.generic import TemplateView
import requests
from environs import Env
env = Env()
env.read_env()


class GetWeatherView(TemplateView):
    template_name = 'myApp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        city = self.request.GET.get('query')
        weather_info = None

        if city:
            weather_info = self.fetch_weather_data(city)
            if 'error' not in weather_info and not weather_info.get('current'):
                weather_info = {'error': "City couldn't be found!"}

        context.update({
            'weather': weather_info,
            'city': city
        })
        return context

    def fetch_weather_data(self, city):
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


