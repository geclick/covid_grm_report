from advanced_filters.admin import AdminAdvancedFiltersMixin
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from import_export import resources, widgets
from import_export.admin import ExportMixin, ImportExportMixin
from import_export.fields import Field
from rangefilter.filter import DateRangeFilter

from . import models, forms

from django.conf import settings
from . import utils

# admin.site.disable_action("delete_selected")


class DataEpidemiologiaResource(resources.ModelResource):

    covid_plus = Field(attribute="covid_plus", column_name="Covid+")
    no_pcr_realizado = Field(
        attribute="no_pcr_realizado", column_name="No PCR Realizado"
    )
    no_muestra = Field(attribute="no_muestra", column_name="No Muestra")
    laboratorio = Field(attribute="laboratorio", column_name="Laboratorio")
    nombre_apellido = Field(
        attribute="nombre_apellido", column_name="Nombres y Apellidos"
    )
    edad = Field(attribute="edad", column_name="Edad")
    sexo = Field(attribute="sexo", column_name="Sexo")
    direccion = Field(attribute="direccion", column_name="Dirección")
    municipio = Field(attribute="municipio", column_name="Municipio")
    aislamiento = Field(attribute="aislamiento", column_name="Aislamiento")
    fis = Field(attribute="fis", column_name="FIS")
    muestra = Field(attribute="muestra", column_name="Muestra")
    ftm = Field(
        attribute="ftm",
        column_name="FTM",
        widget=widgets.DateWidget(format="%d/%m/%Y"),
    )
    fecha_envio = Field(
        attribute="fecha_envio",
        column_name="Fecha Envío",
        widget=widgets.DateWidget(format="%d/%m/%Y"),
    )
    resultado = Field(attribute="resultado", column_name="Resultados")
    fecha_resultado = Field(
        attribute="fecha_resultado",
        column_name="Fecha resultado",
        widget=widgets.DateWidget(format="%d/%m/%Y"),
    )
    hora = Field(
        attribute="hora",
        column_name="Hora resultado",
        widget=widgets.DateWidget(format="HH:mm"),
    )
    pcr_contactos_viajeros = Field(
        attribute="pcr_contactos_viajeros",
        column_name="PCR de los Contactos y Viajeros",
    )
    condicion = Field(attribute="condicion", column_name="Condición")
    pais = Field(attribute="pais", column_name="País")
    observaciones = Field(attribute="observaciones", column_name="Observación")

    class Meta:
        model = models.DataEpidemiologiaModel
        exclude = ("id", "ci_pasaporte")
        export_order = (
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
        verbose_name = "Dato de Epidemiología"
        verbose_name_plural = "Datos de Epidemiologia"


class DataEpidemiologiaAdmin(
    AdminAdvancedFiltersMixin, ExportMixin, admin.ModelAdmin
):
    resource_class = DataEpidemiologiaResource
    list_display = (
        "covid_plus",
        "no_pcr_realizado",
        "no_muestra",
        "laboratorio",
        "nombre_apellido_colored",
        "edad",
        "sexo",
        "direccion",
        "municipio",
        "aislamiento",
        "fis",
        "ftm",
        "muestra",
        "fecha_envio",
        "hora",
        "resultado",
        "fecha_resultado",
        "condicion",
        "pais",
    )
    list_filter = [
        "resultado",
        "fecha_resultado",
        ("fecha_resultado", DateRangeFilter),
        "hora",
        "fecha_envio",
        ("fecha_envio", DateRangeFilter),
        "ftm",
        ("ftm", DateRangeFilter),
        "laboratorio",
        "municipio",
        "sexo",
    ]
    advanced_filter_fields = (
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
        "hora",
        "resultado",
        "fecha_resultado",
        "condicion",
        "pais",
    )
    search_fields = [
        "no_muestra",
        "nombre_apellido__unaccent",
    ]
    ordering = ["-no_muestra"]

    def nombre_apellido_colored(self, obj):
        if obj.resultado is not None and settings.POSITIVE_TEST in obj.resultado:
            color_code = "FF0000"
        else:
            color_code = "000000"

        html = '<span style="color: #{};">{}</span>'.format(
            color_code, obj.nombre_apellido
        )
        return format_html(html)

    nombre_apellido_colored.admin_order_field = "nombre_apellido"
    nombre_apellido_colored.short_description = "Nombres y Apellidos"


class LaboratorioListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _("Laboratorio")

    # Parameter for the filter that will be used in the URL query.
    parameter_name = "laboratorio"

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        laboratorios = models.Laboratorio.objects.values_list("id", "nombre")
        return tuple(laboratorios)

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value():
            queryset = queryset.filter(laboratorio=self.value())

        return queryset


class DataHigieneResource(resources.ModelResource):

    codigo = Field(attribute="codigo", column_name="CÓDIGO")
    id_provincia = Field(attribute="id_provincia", column_name="ID PROVINCIA")
    nombre_apellidos = Field(
        attribute="nombre_apellidos", column_name="NOMBRE Y APELLIDOS"
    )
    edad = Field(attribute="edad", column_name="EDAD")
    sexo = Field(attribute="sexo", column_name="SEXO")
    ci_pasaporte = Field(
        attribute="ci_pasaporte", column_name="C IDENTIDAD/ PASAPORTE"
    )
    direccion = Field(attribute="direccion", column_name="DIRECCION")
    area_salud = Field(attribute="area_salud", column_name="AREA DE SALUD")
    municipio = Field(attribute="municipio", column_name="MUNICIPIO")
    provincia = Field(attribute="provincia", column_name="PROVINCIA")
    condicion = Field(attribute="condicion", column_name="CONDICIÓN")
    pais_procedencia = Field(
        attribute="pais_procedencia", column_name="PAÍS DE PROCEDENCIA"
    )
    f_inicio_sintomas = Field(
        attribute="f_inicio_sintomas", column_name="F INICIO SÍNTOMAS"
    )
    fecha_toma_muestra = Field(
        attribute="fecha_toma_muestra",
        column_name="FECHA DE TOMA DE MUESTRA",
        widget=widgets.DateWidget(format="%d/%m/%Y"),
    )
    tipo_muestra = Field(
        attribute="tipo_muestra", column_name="TIPO DE MUESTRA"
    )
    procedencia_entrega = Field(
        attribute="procedencia_entrega",
        column_name="PROCEDENCIA DE LA ENTREGA",
    )
    resultado = Field(
        attribute="resultado",
        column_name="RESULTADO",
    )
    fecha_inicio_sintomas = Field(
        attribute="fecha_inicio_sintomas",
        column_name="FECHA/ INICIO SÍNTOMAS",
        widget=widgets.DateWidget(format="%d/%m/%Y"),
    )
    ct = Field(attribute="ct", column_name="CT")
    fecha_salida = Field(
        attribute="fecha_salida",
        column_name="FECHA DE SALIDA",
        widget=widgets.DateWidget(format="%d/%m/%Y"),
    )
    laboratorio = Field(attribute="laboratorio", column_name="LABORATORIO")

    class Meta:
        model = models.DataHigieneModel
        exclude = ("id", "processed", "fecha_envio")
        export_order = (
            "codigo",
            "id_provincia",
            "nombre_apellidos",
            "edad",
            "sexo",
            "ci_pasaporte",
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
        verbose_name = "Muestra de Higiene"
        verbose_name_plural = "Muestras de Higiene"

    @utils.overrides(resources.Resource)
    def after_export(self, queryset, data, *args, **kwargs):
        """
        Override to add additional logic. Does nothing by default.
        """

        data.title = "Hoja1"


class DataHigieneAdmin(
    AdminAdvancedFiltersMixin, ExportMixin, admin.ModelAdmin
):
    resource_class = DataHigieneResource
    list_display = (
        "codigo",
        "ci_pasaporte",
        "nombre_apellidos",
        "edad",
        "sexo",
        "provincia",
        "municipio",
        "area_salud",
        "fecha_toma_muestra",
        "laboratorio",
        "fecha_envio",
        "processed",
    )
    list_filter = [
        "laboratorio",
        "sexo",
        "fecha_toma_muestra",
        ("fecha_toma_muestra", DateRangeFilter),
        "fecha_envio",
        ("fecha_envio", DateRangeFilter),
        "processed",
    ]
    advanced_filter_fields = (
        "codigo",
        "nombre_apellidos",
        "ci_pasaporte",
        "fecha_toma_muestra",
        "fecha_envio",
        "laboratorio",
        "municipio",
        "edad",
        "sexo",
        "area_salud",
        "provincia",
    )
    search_fields = [
        "codigo",
        "ci_pasaporte",
        "nombre_apellidos__unaccent",
        "municipio__unaccent",
        "area_salud__unaccent",
    ]
    ordering = ["-codigo"]


class ResultAdmin(admin.ModelAdmin):
    list_display = (
        "fecha",
        "laboratorio",
        "lab_procesado",
        "state",
        "excel_current_path",
    )
    list_filter = [LaboratorioListFilter, "fecha"]
    form = forms.ResultModelForm
    ordering = ["-pk"]


class HigieneUploadAdmin(admin.ModelAdmin):
    list_display = ("laboratorio", "fecha", "state", "excel_current_path")
    list_filter = [LaboratorioListFilter, "fecha"]
    form = forms.HigieneUploadForm
    ordering = ["-pk"]


class EpidemiologiaUploadAdmin(admin.ModelAdmin):
    list_display = ("fecha", "state", "excel_current_path")
    list_filter = ["fecha"]
    form = forms.EpidemiologiaUploadForm
    ordering = ["-pk"]


class ResultRegisterAdmin(admin.ModelAdmin):
    list_display = (
        "sample",
        "nombre_apellido",
        "result",
        "result_date",
        "new_result",
        "new_result_date",
    )
    list_filter = ["result", "result_date"]
    ordering = ["-pk"]

    def nombre_apellido(self, obj):

        return obj.sample.nombre_apellido

    nombre_apellido.short_description = "Nombres y Apellidos"


class MunicipioAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ("city", "province", "lat", "lng", "population")
    list_filter = ["city", "province"]
    search_fields = ["city"]
    ordering = ["pk"]


class CentroAislamientoAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ("user", "nombre", "municipio")
    list_filter = [
        "nombre",
    ]
    ordering = ["pk"]
    autocomplete_fields = ("municipio", "user")


admin.site.register(models.DataEpidemiologiaModel, DataEpidemiologiaAdmin)
admin.site.register(models.DataHigieneModel, DataHigieneAdmin)
admin.site.register(models.Laboratorio)
admin.site.register(models.ResultModel, ResultAdmin)
admin.site.register(models.HigieneUploadModel, HigieneUploadAdmin)
admin.site.register(models.EpidemiologiaUploadModel, EpidemiologiaUploadAdmin)
admin.site.register(models.TestResult)
admin.site.register(models.ResultRegister, ResultRegisterAdmin)
admin.site.register(models.Municipio, MunicipioAdmin)
admin.site.register(models.CentroAislamiento, CentroAislamientoAdmin)
