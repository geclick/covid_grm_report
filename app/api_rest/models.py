from datetime import date, datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from protected_media.models import ProtectedFileField

from django.contrib.auth.models import User

from . import utils

from django.db.models import Manager
from django.db.models.query import QuerySet

from error.models import (
    DataHigieneError,
    DataEpidemiologiaError,
    PlacaErrorModel,
)
from pathlib import Path


class CaseInsensitiveQuerySet(QuerySet):
    def _filter_or_exclude(self, mapper, *args, **kwargs):
        # 'municipio' is a field in your Model whose lookups
        # you want case-insensitive by default
        if "municipio" in kwargs:
            kwargs["municipio__icontains"] = kwargs["municipio"]
            del kwargs["municipio"]
        return super(CaseInsensitiveQuerySet, self)._filter_or_exclude(
            mapper, *args, **kwargs
        )


# custom manager that overrides the initial query set
class ObjectsManager(Manager):
    def get_query_set(self):
        return CaseInsensitiveQuerySet(self.model)


class LabChoices:
    HABANA = "HABANA"
    SANTIAGO = "SANTIAGO"
    ARTEMISA = "ARTEMISA"
    CAMAGUEY = "CAMAGUEY"
    CIEGODEAVILA = "CIEGODEAVILA"
    CIENFUEGOS = "CIENFUEGOS"
    GRANMA = "GRANMA"
    GUANTANMO = "GUANTANAMO"
    HOLGUIN = "HOLGUIN"
    IPK = "IPK"
    MATANZAS = "MATANZAS"
    PINARDELRIO = "PINARDELRIO"
    TUNAS = "TUNAS"
    VILLACLARA = "VILLACLARA"

    choices = [
        (HABANA, "La Habana"),
        (SANTIAGO, "Santiago de Cuba"),
        (ARTEMISA, "Artemisa"),
        (CAMAGUEY, "Camagüey"),
        (CIEGODEAVILA, "Ciego de Ávila"),
        (CIENFUEGOS, "Cienfuegos"),
        (GRANMA, "Granma"),
        (GUANTANMO, "Guantánamo"),
        (HOLGUIN, "Holguín"),
        (IPK, "IPK"),
        (MATANZAS, "Matanzas"),
        (PINARDELRIO, "Pinar del Río"),
        (TUNAS, "Las Tunas"),
        (VILLACLARA, "Villa Clara"),
    ]


class DataHigieneModel(models.Model):
    laboratorio = models.CharField(
        max_length=255,
        verbose_name="Laboratorio enviada",
        choices=LabChoices.choices,
    )
    fecha_envio = models.DateField(
        blank=True, null=True, verbose_name="Fecha del Envío"
    )
    codigo = models.IntegerField(unique=True, verbose_name="Código")
    id_provincia = models.CharField(
        blank=True, null=True, max_length=255, verbose_name="Id Provincia"
    )
    nombre_apellidos = models.CharField(
        max_length=255, verbose_name="Nombre y Apellidos"
    )
    edad = models.IntegerField(blank=True, null=True, verbose_name="Edad")
    sexo = models.CharField(
        blank=True, null=True, max_length=1, verbose_name="Sexo"
    )
    ci_pasaporte = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        verbose_name="C Identidad/ Pasaporte",
    )
    direccion = models.TextField(
        blank=True, null=True, verbose_name="Dirección"
    )
    area_salud = models.CharField(
        blank=True, null=True, max_length=255, verbose_name="Área de Salud"
    )
    municipio = models.CharField(
        blank=True, null=True, max_length=255, verbose_name="Municipio"
    )
    provincia = models.CharField(
        blank=True, null=True, max_length=255, verbose_name="Provincia"
    )
    condicion = models.CharField(
        blank=True, null=True, max_length=255, verbose_name="Condición"
    )
    pais_procedencia = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        verbose_name="País de Procedencia",
    )

    fecha_toma_muestra = models.DateField(
        blank=True, null=True, verbose_name="Fecha de Toma Muestra"
    )
    procedencia_entrega = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        verbose_name="Procedencia de la Entrega",
    )
    tipo_muestra = models.CharField(
        blank=True, null=True, max_length=255, verbose_name="Tipo de Muestreo"
    )
    f_inicio_sintomas = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        verbose_name="Síntomas Iniciales",
    )
    fecha_inicio_sintomas = models.DateField(
        blank=True, null=True, verbose_name="Fecha/ Inicio de Síntomas"
    )
    resultado = models.CharField(
        blank=True,
        null=True,
        default="PENDIENTE",
        max_length=255,
        verbose_name="Resultado",
    )
    ct = models.CharField(
        blank=True, max_length=255, null=True, verbose_name="Ct"
    )
    fecha_salida = models.DateField(
        blank=True, null=True, verbose_name="Fecha de Salida"
    )
    processed = models.BooleanField(
        blank=True, null=True, verbose_name="Procesado", default=False
    )

    objects = ObjectsManager()

    class Meta:
        verbose_name = "Base de datos de muestras"
        verbose_name_plural = "Bases de datos de muestras"
        ordering = ["codigo"]

    def __str__(self):
        return f"{self.codigo}-{self.laboratorio}"


class DataEpidemiologiaModel(models.Model):

    covid_plus = models.IntegerField(
        blank=True, null=True, verbose_name="Covid+"
    )
    no_pcr_realizado = models.IntegerField(
        blank=True, null=True, verbose_name="No PCR Realizado"
    )
    no_muestra = models.IntegerField(unique=True, verbose_name="No Muestra")
    laboratorio = models.CharField(
        max_length=255, verbose_name="Laboratorio", choices=LabChoices.choices
    )
    nombre_apellido = models.CharField(
        max_length=255, verbose_name="Nombres y Apellidos"
    )
    ci_pasaporte = models.CharField(
        blank=True, null=True, max_length=255, verbose_name="Carné o Pasaporte"
    )
    edad = models.IntegerField(blank=True, null=True, verbose_name="Edad")
    sexo = models.CharField(
        blank=True, null=True, max_length=1, verbose_name="Sexo"
    )
    direccion = models.TextField(
        blank=True, null=True, verbose_name="Dirección"
    )
    municipio = models.CharField(
        blank=True, null=True, max_length=255, verbose_name="Municipio"
    )
    aislamiento = models.CharField(
        blank=True, null=True, max_length=255, verbose_name="Aislamiento"
    )
    fis = models.CharField(
        blank=True, null=True, max_length=255, verbose_name="FIS"
    )
    muestra = models.CharField(
        blank=True, null=True, max_length=255, verbose_name="Muestra"
    )
    ftm = models.DateField(blank=True, null=True, verbose_name="FTM")
    fecha_envio = models.DateField(
        blank=True, null=True, verbose_name="Fecha de envío"
    )
    resultado = models.CharField(
        blank=True,
        null=True,
        default="PENDIENTE",
        max_length=255,
        verbose_name="Resultados",
    )
    fecha_resultado = models.DateField(
        blank=True, null=True, verbose_name="Fecha del resultado"
    )
    hora = models.TimeField(
        blank=True, null=True, verbose_name="Hora del resultado"
    )
    pcr_contactos_viajeros = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        verbose_name="PCR de los Contactos y Viajeros",
    )
    condicion = models.CharField(
        blank=True, null=True, max_length=255, verbose_name="Condición"
    )
    pais = models.CharField(
        blank=True, null=True, max_length=255, verbose_name="País"
    )
    observaciones = models.TextField(
        blank=True, null=True, verbose_name="Observaciones"
    )

    objects = ObjectsManager()

    class Meta:
        verbose_name = "Base de datos de resultado"
        verbose_name_plural = "Base de datos de resultados"
        ordering = [
            "no_muestra",
        ]

    def __str__(self):
        return str(self.no_muestra)


class Laboratorio(models.Model):
    nombre = models.CharField(max_length=150)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Nomenclador de Laboratorio"
        verbose_name_plural = "Nomencladores de Laboratorios"
        ordering = [
            "nombre",
        ]


class ResultModel(models.Model):
    fecha = models.DateTimeField(
        default=datetime.now, verbose_name="Fecha del resultado"
    )
    archivo = ProtectedFileField(upload_to=utils.lab_directory_path)
    laboratorio = models.ForeignKey(
        Laboratorio,
        on_delete=models.PROTECT,
        verbose_name="Laboratorio (Enviado)",
        null=False,
    )
    lab_procesado = models.ForeignKey(
        Laboratorio,
        on_delete=models.PROTECT,
        related_name="lab_procesado",
        verbose_name="Laboratorio (Procesado)",
        null=False,
    )

    @property
    def excel_current_path(self):

        current_path = utils.uploaded_file_current_path(
            self.archivo, settings.LAB_DIR_PROCESSED
        )

        return current_path

    excel_current_path.fget.short_description = "Archivo"

    @property
    def state(self):

        path = Path(self.archivo.path)
        error = False
        filename = ""
        if len(path.parts):
            # only name of file without any path, just name and extension
            filename = path.parts[-1]
            error = PlacaErrorModel.objects.filter(
                nombre_archivo=filename
            ).exists()

        current_state = utils.uploaded_file_state(
            self.archivo,
            settings.LAB_DIR_PROCESSED,
            error,
            error_link="/admin/error/placaerrormodel/?nombre_archivo={}".format(  # noqa: E501
                filename
            ),
        )

        return current_state

    state.fget.short_description = "Estado"

    def __str__(self):
        fecha = str(self.fecha)
        return f"{self.laboratorio.nombre}-{fecha}-{self.lab_procesado}"

    class Meta:
        verbose_name = "Cargar resultado"
        verbose_name_plural = "Cargar resultados"
        ordering = ["laboratorio", "fecha"]


class HigieneUploadModel(models.Model):
    fecha = models.DateField(default=date.today, verbose_name="Fecha de envío")
    archivo = ProtectedFileField(upload_to=utils.higiene_directory_path)
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.PROTECT)

    @property
    def excel_current_path(self):

        current_path = utils.uploaded_file_current_path(
            self.archivo, settings.HIGIENE_DIR_PROCESSED
        )

        return current_path

    excel_current_path.fget.short_description = "Archivo"

    @property
    def state(self):
        path = Path(self.archivo.path)
        error = False
        filename = ""
        if len(path.parts):
            # only name of file without any path, just name and extension
            filename = path.parts[-1]
            error = DataHigieneError.objects.filter(
                nombre_archivo=filename
            ).exists()

        current_state = utils.uploaded_file_state(
            self.archivo,
            settings.HIGIENE_DIR_PROCESSED,
            error,
            error_link="/admin/error/datahigieneerror/?nombre_archivo={}".format(  # noqa: E501
                filename
            ),
        )

        return current_state

    state.fget.short_description = "Estado"

    def __str__(self):
        return f"{self.laboratorio.nombre}-{str(self.fecha)}"

    class Meta:
        verbose_name = "Cargar muestra"
        verbose_name_plural = "Cargar muestras"
        ordering = ["laboratorio", "fecha"]


class EpidemiologiaUploadModel(models.Model):
    fecha = models.DateField(default=date.today)
    archivo = ProtectedFileField(upload_to=utils.epidemiologia_directory_path)

    @property
    def excel_current_path(self):

        current_path = utils.uploaded_file_current_path(
            self.archivo, settings.EPIDEMIOLOGIA_DIR_PROCESSED
        )

        return current_path

    excel_current_path.fget.short_description = "Archivo"

    @property
    def state(self):
        path = Path(self.archivo.path)
        error = False
        filename = ""
        if len(path.parts):
            # only name of file without any path, just name and extension
            filename = path.parts[-1]
            error = DataEpidemiologiaError.objects.filter(
                nombre_archivo=filename
            ).exists()
        current_state = utils.uploaded_file_state(
            self.archivo,
            settings.EPIDEMIOLOGIA_DIR_PROCESSED,
            error,
            error_link="/admin/error/dataepidemiologiaerror/?nombre_archivo={}".format(  # noqa: E501
                filename
            ),
        )

        return current_state

    state.fget.short_description = "Estado"

    def __str__(self):
        return f"bd-{str(self.fecha)}"

    class Meta:
        verbose_name = "Restaurar resultado"
        verbose_name_plural = "Restaurar resultados"
        ordering = ["fecha"]


class TestResult(models.Model):

    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Nomenclador de resultado de PCR"
        verbose_name_plural = "Nomenclador de resultado de PCR"


@receiver(post_save, sender=DataHigieneModel)
def actualiza_epidemiologia(sender, instance=None, created=False, **kwargs):

    data = utils.epidemiologia_data_map(instance)

    if created:
        if not DataEpidemiologiaModel.objects.exists():
            no = 1
            covid = 1
            data.update({"no_pcr_realizado": no, "covid_plus": covid})
        else:
            last = (
                DataEpidemiologiaModel.objects.exclude(no_pcr_realizado=None)
                .order_by("no_pcr_realizado")
                .last()
            )
            no = last.no_pcr_realizado + 1
            try:
                covid = last.covid_plus + 1
                data.update({"no_pcr_realizado": no, "covid_plus": covid})
            except TypeError:
                data.update({"no_pcr_realizado": no})

    DataEpidemiologiaModel.objects.update_or_create(
        no_muestra=instance.codigo,
        defaults=data,
    )


class ResultRegister(models.Model):
    sample = models.ForeignKey(
        DataEpidemiologiaModel,
        on_delete=models.PROTECT,
        verbose_name="Muestra",
    )
    result = models.CharField(max_length=255, verbose_name="Resultado")
    result_date = models.DateField(verbose_name="Fecha de resultado")
    new_result = models.CharField(
        max_length=255, verbose_name="Nuevo resultado", blank=True
    )
    new_result_date = models.DateField(
        verbose_name="Nueva fecha de resultado", null=True
    )

    def __str__(self):
        return f"{self.sample.no_muestra}-{self.result}-{self.result_date}"

    class Meta:
        verbose_name = "Registro de resultados de una muestra"
        verbose_name_plural = "Registro de resultados de una muestra"


class Municipio(models.Model):
    city = models.CharField(max_length=255, verbose_name="Nombre")
    lat = models.DecimalField(
        verbose_name="Latitud", null=True, max_digits=8, decimal_places=5
    )
    lng = models.DecimalField(
        verbose_name="Longitud", null=True, max_digits=8, decimal_places=5
    )
    country = models.CharField(
        max_length=255, verbose_name="Pais", default="Cuba", blank=True
    )
    province = models.CharField(
        max_length=255, verbose_name="Provincia", blank=True
    )
    population = models.PositiveIntegerField(
        verbose_name="Habitantes", null=True
    )

    def __str__(self):
        return "{} ({})".format(self.city, self.province)

    class Meta:
        verbose_name = "Municipio"
        verbose_name_plural = "Municipios"


class CentroAislamiento(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Nombre del Centro")
    municipio = models.ForeignKey(
        Municipio, on_delete=models.PROTECT, null=True
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="centro", null=True
    )

    def __str__(self):
        return "{} ({})".format(self.nombre, self.user.get_full_name())

    class Meta:
        verbose_name = "Centro de Aislamiento"
        verbose_name_plural = "Centros de Aislamiento"


@receiver(post_save, sender=User)
def create_user_centro_aislamiento(sender, instance, created, **kwargs):
    if created:
        CentroAislamiento.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_centro_aislamiento(sender, instance, **kwargs):
    try:
        instance.centro.save()
    except ObjectDoesNotExist:
        CentroAislamiento.objects.create(user=instance)
