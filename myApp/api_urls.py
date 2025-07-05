from . import api_views
from django.urls import path, include

app_name = 'myApp'

urlpatterns = [
    path('weather/', api_views.WeatherAPIView.as_view(), name='weather'),
]