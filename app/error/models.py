from django.db import models
from django.conf import settings

from api_rest import utils


class DataHigieneError(models.Model):
    msg = models.TextField(verbose_name="Causa")
    nombre_archivo = models.CharField(max_length=255, verbose_name="Archivo")
    fecha = models.DateField(
        auto_now_add=True, verbose_name="Fecha en que se procesó el archivo"
    )
    laboratorio = models.CharField(
        null=True, blank=True, max_length=255, verbose_name="Laboratorio"
    )
    codigo = models.CharField(
        null=True, blank=True, max_length=255, verbose_name="Código"
    )
    ci_pasaporte = models.CharField(
        null=True, blank=True, max_length=255, verbose_name="CI o Pasaporte"
    )
    fecha_toma_muestra = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name="Fecha de Toma Muestra",
    )
    edad = models.CharField(
        null=True, blank=True, max_length=255, verbose_name="Edad"
    )
    sexo = models.CharField(
        null=True, blank=True, max_length=255, verbose_name="Sexo"
    )
    nombre_apellidos = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        verbose_name="Nombres y Apellidos",
    )
    condicion = models.CharField(
        null=True, blank=True, max_length=255, verbose_name="Condición"
    )
    direccion = models.TextField(
        null=True, blank=True, verbose_name="Dirección"
    )
    municipio = models.CharField(
        null=True, blank=True, max_length=255, verbose_name="Municipio"
    )
    provincia = models.CharField(
        null=True, blank=True, max_length=255, verbose_name="Provincia"
    )
    id_provincia = models.CharField(
        null=True, blank=True, max_length=255, verbose_name="id_provincia"
    )
    pais_procedencia = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name="País de Procedencia",
    )
    procedencia_entrega = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name="Procedencia de la Entrega",
    )
    area_salud = models.CharField(
        null=True, blank=True, max_length=255, verbose_name="Área de salud"
    )
    f_inicio_sintomas = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name="Síntomas iniciales",
    )
    tipo_muestra = models.CharField(
        null=True, blank=True, max_length=255, verbose_name="Tipo de muestreo"
    )
    fecha_inicio_sintomas = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name="Fecha inicio de síntomas",
    )
    ct = models.CharField(
        null=True, blank=True, max_length=255, verbose_name="CT"
    )
    fecha_salida = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name="Fecha del resultado",
    )
    fecha_envio = models.DateField(
        blank=True, null=True, verbose_name="Fecha del Envío"
    )

    class Meta:
        verbose_name = "Error de procesamiento de archivo de muestra"
        verbose_name_plural = "Errores de procesamiento de archivo de muestras"
        ordering = [
            "pk",
        ]

    def __str__(self):
        return f"{self.msg}-{self.fecha}-{self.archivo}"

    @property
    def archivo(self):
        """
        Return path to higiene file
        """
        path = (
            f"{settings.PROTECTED_MEDIA_ROOT}/{settings.HIGIENE_DIR_PROCESSED}"
        )
        filename = utils.error_filename_path(
            self.nombre_archivo, path, settings.HIGIENE_DIR_PROCESSED
        )

        return filename


class DataEpidemiologiaError(models.Model):
    msg = models.TextField(verbose_name="Causa")
    nombre_archivo = models.CharField(max_length=255, verbose_name="Archivo")
    fecha = models.DateField(
        auto_now_add=True, verbose_name="Fecha en que se procesó el archivo"
    )
    covid_plus = models.CharField(
        blank=True, max_length=255, verbose_name="Covid+", null=True
    )
    no_pcr_realizado = models.CharField(
        blank=True, max_length=255, verbose_name="No PCR Realizado", null=True
    )
    no_muestra = models.CharField(
        blank=True, max_length=255, verbose_name="No Muestra", null=True
    )
    laboratorio = models.CharField(
        blank=True, max_length=255, verbose_name="Laboratorio", null=True
    )
    nombre_apellido = models.CharField(
        blank=True,
        max_length=255,
        verbose_name="Nombres y Apellidos",
        null=True,
    )
    ci_pasaporte = models.CharField(
        blank=True, null=True, max_length=255, verbose_name="Carné o Pasaporte"
    )
    edad = models.CharField(
        blank=True, max_length=255, verbose_name="Edad", null=True
    )
    sexo = models.CharField(
        blank=True, null=True, max_length=255, verbose_name="Sexo"
    )
    direccion = models.TextField(
        blank=True, null=True, verbose_name="Dirección"
    )
    municipio = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        verbose_name="Municipio",
    )
    aislamiento = models.CharField(
        blank=True, null=True, max_length=255, verbose_name="Aislamiento"
    )
    fis = models.CharField(
        blank=True, null=True, max_length=255, verbose_name="FIS"
    )
    muestra = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        verbose_name="Muestra",
    )
    ftm = models.CharField(
        blank=True, max_length=255, verbose_name="FTM", null=True
    )
    fecha_envio = models.CharField(
        blank=True, max_length=255, verbose_name="Fecha de envío", null=True
    )
    resultado = models.CharField(
        blank=True,
        default="PENDIENTE",
        max_length=255,
        verbose_name="Resultados",
        null=True,
    )
    fecha_resultado = models.CharField(
        blank=True,
        max_length=255,
        verbose_name="Fecha del resultado",
        null=True,
    )
    pcr_contactos_viajeros = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        verbose_name="PCR de los Contactos y Viajeros",
    )
    condicion = models.CharField(
        blank=True, max_length=255, verbose_name="Condición", null=True
    )
    pais = models.CharField(
        blank=True, max_length=255, verbose_name="País", null=True
    )
    observaciones = models.TextField(
        blank=True, verbose_name="Observaciones", null=True
    )

    hora = models.CharField(
        blank=True, max_length=10, verbose_name="Hora del resultado", null=True
    )

    hora = models.CharField(
        blank=True, max_length=10, verbose_name="Hora del resultado", null=True)

    class Meta:
        verbose_name = "Error de procesamiento de archivo \
            de restauración de resultados"
        verbose_name_plural = "Error de procesamiento de archivos \
            de restauración de resultados"
        ordering = [
            "pk",
        ]

    def __str__(self):
        return f"{self.msg}-{self.fecha}-{self.archivo}"

    @property
    def archivo(self):
        """
        Return path to epidemiologia file
        """
        path = f"{settings.PROTECTED_MEDIA_ROOT}/{settings.EPIDEMIOLOGIA_DIR_PROCESSED}"  # noqa: E501
        filename = utils.error_filename_path(
            self.nombre_archivo, path, settings.EPIDEMIOLOGIA_DIR_PROCESSED
        )

        return filename


class PlacaErrorModel(models.Model):
    msg = models.TextField(verbose_name="Causa")
    nombre_archivo = models.CharField(max_length=255, verbose_name="Archivo")
    fecha = models.DateField(
        auto_now_add=True, verbose_name="Fecha en que se procesó el archivo"
    )
    laboratorio = models.CharField(
        null=True, blank=True, max_length=255, verbose_name="Laboratorio"
    )
    no_muestra = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name="Código",
    )
    ci = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name="CI o Pasaporte",
    )
    edad = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name="Edad",
    )
    sexo = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name="Sexo",
    )
    nombre_apellidos = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name="Nombres y Apellidos",
    )
    municipio = models.CharField(
        null=True, blank=True, max_length=255, verbose_name="Municipio"
    )
    provincia = models.CharField(
        null=True, blank=True, max_length=255, verbose_name="Provincia"
    )
    resultado = models.CharField(
        null=True, blank=True, max_length=255, verbose_name="Resultado"
    )
    fecha_resultado = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name="Fecha del resultado",
    )
    hora = models.CharField(
        blank=True, max_length=10, verbose_name="Hora del resultado", null=True
    )
    hora = models.CharField(
        blank=True, max_length=10, verbose_name="Hora del resultado", null=True)
    observaciones = models.TextField(
        blank=True, null=True, verbose_name="Observaciones"
    )

    class Meta:
        verbose_name = "Error de procesamiento de archivo de resultados"
        verbose_name_plural = "Errores de procesamiento de \
            archivos de resultados"
        ordering = [
            "pk",
        ]

    def __str__(self):
        return f"{self.msg}-{self.fecha}-{self.archivo}"

    @property
    def archivo(self):
        """
        Return path to placa file
        """
        path = f"{settings.PROTECTED_MEDIA_ROOT}/{settings.LAB_DIR}"
        filename = utils.error_filename_path(
            self.nombre_archivo, path, settings.LAB_DIR_PROCESSED
        )

        return filename
