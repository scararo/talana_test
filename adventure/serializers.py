from rest_framework import serializers


class JourneySerializer(serializers.Serializer):
    name = serializers.CharField()
    passengers = serializers.IntegerField()
    number_plate = serializers.CharField()


class StopJourneySerializer(serializers.Serializer):
    id = serializers.IntegerField()