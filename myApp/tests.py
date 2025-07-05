from django.test import TestCase
from unittest.mock import patch
from myApp.views import fetch_weather_for_city
from requests.exceptions import RequestException

class WeatherTests(TestCase):

    @patch('myApp.views.requests.get')
    def test_fetch_weather_uses_cache(self, mock_get):
        fake_data = {'location': {'name': 'London'}, 'current': {'temp_c': 20}}

        mock_get.return_value.json.return_value = fake_data
        mock_get.return_value.raise_for_status = lambda: None

        resutlt = fetch_weather_for_city('London')
        self.assertEqual(resutlt, fake_data)


    def test_fetch_weather_handles_api_error(self):
        city = 'InvalidCity'

        with patch('myApp.views.requests.get') as mock_get:
            mock_get.side_effect = RequestException("API error")
            result = fetch_weather_for_city(city)

            self.assertIn('error', result)
            self.assertIn('An error occurred', result['error'])
