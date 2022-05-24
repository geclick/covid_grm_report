from rest_framework import serializers

from . import models


class DataHigieneErrorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DataHigieneError
        fields = "__all__"


class DataEpidemiologiaErrorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DataEpidemiologiaError
        fields = "__all__"


class PlacaErrorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PlacaErrorModel
        fields = "__all__"
