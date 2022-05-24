from . import models
import django_filters

# DataHigieneModel Filters regions


class DataHigieneFilter(django_filters.FilterSet):
    nombre_apellidos = django_filters.CharFilter(lookup_expr="icontains")
    ci_pasaporte = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = models.DataHigieneModel
        fields = "__all__"


# DataEpidemiologiaModel Filters regions


class DataEpidemiologiaFilter(django_filters.FilterSet):
    nombre_apellido = django_filters.CharFilter(lookup_expr="icontains")
    ci_pasaporte = django_filters.CharFilter(lookup_expr="icontains")
    municipio = django_filters.CharFilter(lookup_expr="icontains")
    aislamiento = django_filters.CharFilter(lookup_expr="icontains")
    condicion = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = models.DataEpidemiologiaModel
        fields = (
            "covid_plus",
            "no_pcr_realizado",
            "no_muestra",
            "laboratorio",
            "nombre_apellido",
            "edad",
            "sexo",
            "direccion",
            "municipio",
            "aislamiento",
            "fis",
            "ftm",
            "muestra",
            "fecha_envio",
            "resultado",
            "fecha_resultado",
            "hora",
            "pcr_contactos_viajeros",
            "condicion",
            "pais",
            "observaciones",
        )


class MunicipioFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(lookup_expr="icontains")
    province = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = models.Municipio
        fields = "__all__"
