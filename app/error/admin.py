from urllib.parse import urlencode

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import path, reverse
from django.utils.html import format_html

from api_rest import models as api_rest_models
from api_rest.admin import DataEpidemiologiaResource, DataHigieneResource
from . import models

from import_export import resources
from import_export.admin import ExportMixin
from import_export.fields import Field
from advanced_filters.admin import AdminAdvancedFiltersMixin
from django.conf import settings

from api_rest import utils


class DataErrorHigieneResource(DataHigieneResource):
    fecha_toma_muestra = Field(
        attribute="fecha_toma_muestra", column_name="FECHA DE TOMA DE MUESTRA"
    )
    fecha_inicio_sintomas = Field(
        attribute="fecha_inicio_sintomas", column_name="FECHA/INICIO SÍNTOMAS"
    )
    fecha_salida = Field(
        attribute="fecha_salida", column_name="FECHA DE SALIDA"
    )


class DataHigieneErrorAdmin(
    AdminAdvancedFiltersMixin, ExportMixin, admin.ModelAdmin
):
    resource_class = DataErrorHigieneResource
    list_display = (
        "codigo",
        "laboratorio",
        "nombre_apellidos",
        "msg",
        "fecha",
        "path",
        "custom_actions",
    )
    list_display_links = ("msg",)
    list_filter = ["laboratorio", "fecha_envio", "msg"]
    advanced_filter_fields = (
        "fecha_envio",
        "laboratorio",
        "msg",
    )

    search_fields = [
        "msg",
    ]

    list_per_page = 1000

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path(
                "fix/<int:pk>/",
                self.fix_data,
                name="api_rest_datahigienemodel_fix",
            ),
        ]
        return my_urls + urls

    def fix_data(self, request, pk):
        error = get_object_or_404(models.DataHigieneError, pk=pk)
        match = DataMatch(error)
        data = match(api_rest_models.DataHigieneModel)

        base_url = reverse("admin:api_rest_datahigienemodel_add")
        query = urlencode(data)
        url = f"{base_url}?{query}"

        return HttpResponseRedirect(url)

    def path(self, obj):
        name = obj.nombre_archivo
        url = obj.archivo

        return format_html(f'<a href="{url}" "target="_blank">{name}</a>')

    def custom_actions(self, obj):
        url = reverse("admin:api_rest_datahigienemodel_fix", args=[obj.pk])
        return format_html(
            '<a class="button" href="{}" target="blank">Corregir</a>', url
        )

    custom_actions.short_description = "Acciones"
    custom_actions.allow_tags = True
    path.short_description = "Archivo fuente"


admin.site.register(models.DataHigieneError, DataHigieneErrorAdmin)


class DataErrorEpidemiologiaResource(DataEpidemiologiaResource):
    ftm = Field(attribute="ftm", column_name="FTM")
    fecha_envio = Field(
        attribute="fecha_envio",
        column_name="Fecha Envío",
    )
    fecha_resultado = Field(
        attribute="fecha_resultado",
        column_name="Fecha resultado",
    )


class DataEpidemiologiaErrorAdmin(
    AdminAdvancedFiltersMixin, ExportMixin, admin.ModelAdmin
):
    resource_class = DataErrorEpidemiologiaResource
    list_display = (
        "no_muestra",
        "laboratorio",
        "nombre_apellido",
        "resultado",
        "msg",
        "fecha",
        "path",
        "custom_actions",
    )
    list_display_links = ("msg",)
    list_filter = [
        "fecha",
        "laboratorio",
        "nombre_archivo",
        "msg",
    ]
    advanced_filter_fields = (
        "no_muestra",
        "fecha",
        "laboratorio",
        "nombre_archivo",
        "msg",
    )
    search_fields = [
        "nombre_apellido",
        "msg",
    ]
    list_per_page = 1000

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path(
                "fix/<int:pk>/",
                self.fix_data,
                name="api_rest_dataepidemiologiamodel_fix",
            ),
        ]
        return my_urls + urls

    def fix_data(self, request, pk):
        error = get_object_or_404(models.DataEpidemiologiaError, pk=pk)
        match = DataMatch(error)
        data = match(api_rest_models.DataEpidemiologiaModel)

        base_url = reverse("admin:api_rest_dataepidemiologiamodel_add")
        query = urlencode(data)
        url = f"{base_url}?{query}"

        return HttpResponseRedirect(url)

    def path(self, obj):
        name = obj.nombre_archivo
        url = obj.archivo

        return format_html(f'<a href="{url}" "target="_blank">{name}</a>')

    def custom_actions(self, obj):
        url = reverse(
            "admin:api_rest_dataepidemiologiamodel_fix", args=[obj.pk]
        )
        return format_html(
            '<a class="button" href="{}" target="blank">Corregir</a>', url
        )

    custom_actions.short_description = "Acciones"
    custom_actions.allow_tags = True
    path.short_description = "Archivo fuente"


admin.site.register(models.DataEpidemiologiaError, DataEpidemiologiaErrorAdmin)


class PlacaErrorResource(resources.ModelResource):
    codigo = Field(column_name="CÓDIGO")
    id_provincia = Field(column_name="ID PROVINCIA")
    nombre_apellidos = Field(
        attribute="nombre_apellidos", column_name="NOMBRE Y APELLIDOS"
    )
    edad = Field(attribute="edad", column_name="EDAD")
    sexo = Field(attribute="sexo", column_name="SEXO")
    ci = Field(attribute="ci", column_name="C IDENTIDAD/ PASAPORTE")
    direccion = Field(column_name="DIRECCION")
    area_salud = Field(column_name="AREA DE SALUD")
    municipio = Field(attribute="municipio", column_name="MUNICIPIO")
    provincia = Field(attribute="provincia", column_name="PROVINCIA")
    condicion = Field(column_name="CONDICIÓN")
    pais_procedencia = Field(column_name="PAÍS DE PROCEDENCIA")
    f_inicio_sintomas = Field(column_name="F INICIO SÍNTOMAS")
    fecha_toma_muestra = Field(column_name="FECHA DE TOMA DE MUESTRA")
    tipo_muestra = Field(column_name="TIPO DE MUESTRA")
    procedencia_entrega = Field(column_name="PROCEDENCIA DE LA ENTREGA")
    resultado = Field(column_name="RESULTADO", default="PENDIENTE")
    fecha_inicio_sintomas = Field(column_name="FECHA/ INICIO SÍNTOMAS")
    ct = Field(column_name="CT")
    fecha_salida = Field(column_name="FECHA DE SALIDA")

    class Meta:
        model = models.PlacaErrorModel
        exclude = (
            "no_muestra",
            "id",
            "fecha_resultado",
            "hora",
            "observaciones",
            "msg",
            "nombre_archivo",
            "fecha",
            "laboratorio",
        )
        export_order = (
            "codigo",
            "id_provincia",
            "nombre_apellidos",
            "edad",
            "sexo",
            "ci",
            "direccion",
            "area_salud",
            "municipio",
            "provincia",
            "condicion",
            "pais_procedencia",
            "f_inicio_sintomas",
            "fecha_toma_muestra",
            "tipo_muestra",
            "procedencia_entrega",
            "resultado",
            "fecha_inicio_sintomas",
            "ct",
            "fecha_salida",
        )

    @utils.overrides(resources.Resource)
    def after_export(self, queryset, data, *args, **kwargs):
        """
        Override to add additional logic. Does nothing by default.
        """

        data.title = "Hoja1"

    def dehydrate_resultado(self, placa):
        return settings.PENDING_TEST

    def dehydrate_id_provincia(self, placa):
        return settings.COUNTRY_PROVINCE


class PlacaErrorAdmin(
    AdminAdvancedFiltersMixin, ExportMixin, admin.ModelAdmin
):
    resource_class = PlacaErrorResource
    list_display = (
        "no_muestra",
        "laboratorio",
        "nombre_apellidos",
        "resultado",
        "msg",
        "fecha",
        "path",
    )
    list_display_links = ("msg",)
    list_filter = [
        "resultado",
        "fecha",
        "laboratorio",
        "nombre_archivo",
        "msg",
    ]
    advanced_filter_fields = (
        "msg",
        "resultado",
        "fecha",
        "laboratorio",
        "nombre_archivo",
    )
    search_fields = [
        "nombre_apellidos",
        "msg",
    ]
    list_per_page = 1000

    def path(self, obj):
        name = obj.nombre_archivo
        url = obj.archivo

        return format_html(f'<a href="{url}">{name}</a>')

    path.short_description = "Archivo fuente"


admin.site.register(models.PlacaErrorModel, PlacaErrorAdmin)


class DataMatch:
    """
    Render html data higiene form with hidden fields.

    Field values are taken form error object.

    Args:
        obj (django.db.models.Model): model instance
    """

    def __init__(self, instance):
        self.error = instance

    def __call__(self, model_class):
        """
        Return subdata in model class fields

        Args:
            model_class (type(models.Model)): model class
        """
        class_fields = model_class._meta.get_fields()
        class_fields = [field.name for field in class_fields]
        instance_fields = self.error.__class__._meta.get_fields()
        instance_fields = [field.name for field in instance_fields]
        fields = [field for field in class_fields if field in instance_fields]
        fields.remove("id")

        data = {
            field: getattr(self.error, field)
            for field in fields
            if getattr(self.error, field)
        }
        return data
