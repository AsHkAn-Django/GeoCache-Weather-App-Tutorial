from rest_framework import serializers


class LatLonSerializer(serializers.Serializer):
    latitude = serializers.DecimalField(max_digits=8, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=8, decimal_places=6)