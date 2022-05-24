from datetime import datetime

from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.http import Http404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters
from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound

# from rest_framework.permissions import (
#     AllowAny, IsAuthenticated, DjangoModelPermissions
# )
from rest_framework.response import Response

from .filters import (
    DataEpidemiologiaFilter,
    DataHigieneFilter,
    MunicipioFilter,
)
from .models import DataEpidemiologiaModel, DataHigieneModel, Municipio
from .serializer import (
    DataEpidemiologiaSerializer,
    DataEpidemiologiaColorRowSerializer,
    DataHigieneSerializer,
    MunicipioSerializer,
)
from . import utils, permissions
from . import helpers
from rest_framework.viewsets import ReadOnlyModelViewSet
from drf_renderer_xlsx.renderers import XLSXRenderer
from drf_renderer_xlsx.mixins import XLSXFileMixin


def index(request):
    return HttpResponseRedirect("/admin")


class UpsertMixin(object):
    """
    The following mixin class may be used in order to support PUT-as-create
    behavior for incoming requests.
    """

    def get_object_for_upsert(self):
        """
        Returns the object for upsert.
        """
        data = self.request.data
        queryset = self.filter_queryset(self.get_queryset())

        try:
            assert self.lookup_field in data

            filter_kwargs = {self.lookup_field: data[self.lookup_field]}
            obj = get_object_or_404(queryset, **filter_kwargs)
            # May raise a permission denied
            self.check_object_permissions(self.request, obj)

            return obj
        except (Http404, AssertionError):
            pass

    def create(self, request, *args, **kwargs):
        instance = self.get_object_for_upsert()

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        status_201 = status.HTTP_201_CREATED
        swargs = {"status": status_201} if instance is None else {}
        return Response(serializer.data, **swargs)


class DataHigieneViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.AuthorizedAccessPermissions]
    queryset = DataHigieneModel.objects.all()
    serializer_class = DataHigieneSerializer
    lookup_field = "codigo"
    filterset_class = DataHigieneFilter
    filter_backends = [filters.SearchFilter]
    ordering_fields = "__all__"


class DataEpidemiologiaViewset(UpsertMixin, viewsets.ModelViewSet):
    permission_classes = [permissions.AuthorizedAccessPermissions]
    queryset = DataEpidemiologiaModel.objects.all()
    serializer_class = DataEpidemiologiaSerializer
    lookup_field = "no_muestra"
    filterset_class = DataEpidemiologiaFilter
    ordering_fields = "__all__"


class LabViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AddPlacaPermissions]

    @swagger_auto_schema(
        operation_description="Subir una placa con los resultados del PCR"
        + " del paciente.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[
                "laboratorio",
                "nombre_apellidos",
                "resultado",
                "fecha_resultado",
                "provincia",
            ],
            properties={
                "no_muestra": openapi.Schema(type=openapi.TYPE_INTEGER),
                "laboratorio": openapi.Schema(type=openapi.TYPE_STRING),
                "nombre_apellidos": openapi.Schema(type=openapi.TYPE_STRING),
                "ci": openapi.Schema(type=openapi.TYPE_STRING),
                "edad": openapi.Schema(type=openapi.TYPE_INTEGER),
                "sexo": openapi.Schema(
                    type=openapi.TYPE_STRING, default="M", max_length=1
                ),
                "provincia": openapi.Schema(type=openapi.TYPE_STRING),
                "municipio": openapi.Schema(type=openapi.TYPE_STRING),
                "resultado": openapi.Schema(type=openapi.TYPE_STRING),
                "ct": openapi.Schema(type=openapi.TYPE_STRING),
                "fecha_resultado": openapi.Schema(
                    type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE
                ),
                "hora": openapi.Schema(
                    type=openapi.TYPE_STRING, default="00:00"
                ),
            },
        ),
        security=[],
        responses={
            "400": "Validation error.",
            "404": "Registro no encontrado",
            "200": "Success",
        },
    )
    def create(self, request):
        config = utils.LabViesetConfig()

        filters = config.filters(request.data)
        data_higiene = DataHigieneModel.objects.filter(**filters).last()

        if not data_higiene:
            msg = (
                "La muestra no esta registrada en la base de datos, "
                + "verifique!!!"
            )
            raise NotFound(detail=msg)

        # if data_higiene.processed:
        #     raise NotFound(detail='Registro de higiene encontrado \
        #         pero ya fué procesado')

        try:
            data_epidemiologia = DataEpidemiologiaModel.objects.get(
                no_muestra=data_higiene.codigo
            )
        except DataEpidemiologiaModel.DoesNotExist:
            data_map = utils.epidemiologia_data_map(data_higiene)
            if not DataEpidemiologiaModel.objects.exists():
                data_map.update({"no_pcr_realizado": 1, "covid_plus": 1})
            else:
                last = DataEpidemiologiaModel.objects.order_by(
                    "no_pcr_realizado"
                ).last()
                no = last.no_pcr_realizado + 1
                covid = last.covid_plus
                data_map.update({"no_pcr_realizado": no, "covid_plus": covid})

            data_epidemiologia = DataEpidemiologiaModel.objects.create(
                **data_map
            )

        data = config.data(request.data)
        serializer = helpers.diagnose(data_epidemiologia, **data)

        data_higiene.processed = True
        data_higiene.save()

        return Response(serializer.data)

    # def get_permissions(self):
    #     """
    #     Instantiates and returns the list of permissions that this view
    #     requires.
    #     """
    #
    #     permission_classes = [permissions.AddPlacaPermissions]
    #     return [permission() for permission in permission_classes]


class EpidemiologiaXLSView(XLSXFileMixin, ReadOnlyModelViewSet):
    permission_classes = [permissions.AuthorizedAccessPermissions]
    # permission_classes = [IsAuthenticated]
    renderer_classes = [XLSXRenderer]
    serializer_class = DataEpidemiologiaColorRowSerializer
    queryset = DataEpidemiologiaModel.objects.all()
    filterset_class = DataEpidemiologiaFilter

    today = datetime.today().strftime("%d-%m-%Y")
    filename = f"epidemiologia-{today}.xlsx"

    column_header = {
        "titles": [
            "Covid+",
            "No PCR Realizado",
            "No Muestra",
            "Laboratorio",
            "Nombres y Apellidos",
            "Edad",
            "Sexo",
            "Dirección",
            "Municipio",
            "Aislamiento",
            "FIS",
            "FTM",
            "Muestra",
            "Fecha envío",
            "Resultados",
            "Fecha resultado",
            "Hora resultado",
            "PCR de los Contactos y Viajeros",
            "Condición",
            "País",
            "Observación",
        ],
        "column_width": [
            8,
            18,
            12,
            12,
            30,
            8,
            8,
            30,
            12,
            30,
            40,
            12,
            12,
            12,
            12,
            16,
            16,
            30,
            30,
            12,
            30,
        ],
        "height": 18,
        "style": {
            "fill": {
                "fill_type": "solid",
                "start_color": "FFCCFFCC",
            },
            "alignment": {
                "horizontal": "center",
                "vertical": "center",
                "wrapText": True,
                "shrink_to_fit": True,
            },
            "border_side": {
                "border_style": "thin",
                "color": "FF000000",
            },
            "font": {
                "name": "Arial",
                "size": 10,
                "bold": True,
                "color": "FF000000",
            },
        },
    }
    body = {
        "style": {
            "alignment": {
                "horizontal": "center",
                "vertical": "center",
                "wrapText": True,
                "shrink_to_fit": True,
            },
            "border_side": {
                "border_style": "thin",
                "color": "FF000000",
            },
            "font": {
                "name": "Arial",
                "size": 10,
                "bold": False,
                "color": "FF000000",
            },
        },
        "height": 18,
    }

    def filter_queryset(self, queryset):
        queryset = super(EpidemiologiaXLSView, self).filter_queryset(queryset)
        return queryset.order_by("no_pcr_realizado")


class MunicipioViewset(UpsertMixin, viewsets.ModelViewSet):
    queryset = Municipio.objects.all()
    serializer_class = MunicipioSerializer
    lookup_field = "city"
    filterset_class = MunicipioFilter
    ordering_fields = "__all__"
    permission_classes = [permissions.AuthorizedAccessPermissions]
