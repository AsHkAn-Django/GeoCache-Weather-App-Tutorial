from django.urls import path
from .views import GetWeatherView, receive_coordinates

app_name = 'myApp'

urlpatterns = [
    path('search/', GetWeatherView.as_view(), name='get_weather'),
    path("", receive_coordinates, name="send_coordinates"),
]