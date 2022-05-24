from rest_framework import viewsets
from django.shortcuts import render

from . import models
from . import serializers
from api_rest.permissions import AuthorizedAccessPermissions


class DataHigieneErrorViewset(viewsets.ModelViewSet):
    permission_classes = [AuthorizedAccessPermissions]
    queryset = models.DataHigieneError.objects.all()
    serializer_class = serializers.DataHigieneErrorSerializer


class DataEpidemiologiaErrorViewset(viewsets.ModelViewSet):
    permission_classes = [AuthorizedAccessPermissions]
    queryset = models.DataEpidemiologiaError.objects.all()
    serializer_class = serializers.DataEpidemiologiaErrorSerializer


class PlacaErrorViewset(viewsets.ModelViewSet):
    permission_classes = [AuthorizedAccessPermissions]
    queryset = models.PlacaErrorModel.objects.all()
    serializer_class = serializers.PlacaErrorSerializer


def error_403(request, exception=None):
    data = {}
    return render(request, "error/403.html", data, status=403)


def error_400(request, exception=None):
    data = {"code": 400, "message": "Petición incorrecta", "enc": ""}
    return render(request, "error/404.html", data, status=400)


def error_404(request, exception=None):
    data = {"code": 404, "message": "NO FUE ENCONTRADO", "enc": "EL RECURSO"}
    return render(request, "error/404.html", data, status=404)


def error_500(request, exception=None):
    data = {}
    return render(request, "error/50x.html", data, status=500)
