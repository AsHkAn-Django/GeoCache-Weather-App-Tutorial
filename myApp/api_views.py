from rest_framework.views import APIView
from .serializers import LatLonSerializer
from rest_framework.response import Response



class WeatherAPIView(APIView):

    def get(self, request, format=None):
        lat = request.query_params.get('lat')
        lon = request.query_params.get('lon')
        return Response({'Result': f'your lat is {lat} and you lon is {lon}'})