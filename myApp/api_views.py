from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .views import fetch_weather_for_cord
from .serializers import LatLonSerializer


class WeatherAPIView(APIView):
    """Accepts latitude and longitude in url as parameters to return weather condition for that location."""
    # GET /api/v1/weather/?latitude=37.758021&longitude=30.529230

    def get(self, request, format=None):
        data = request.query_params.dict()

        serializer = LatLonSerializer(data=data)
        if serializer.is_valid():
            valid_lat = serializer.validated_data['latitude']
            valid_lon = serializer.validated_data['longitude']
            cache_key = f"weather_{valid_lat}_{valid_lon}"
            location_weather = fetch_weather_for_cord(valid_lat, valid_lon, cache_key)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'latitude': valid_lat, 'longtitude': valid_lon, 'weather': location_weather})