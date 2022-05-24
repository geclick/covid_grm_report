from datetime import date

import factory
from factory import DjangoModelFactory

from error import models


class DataHigieneErrorFactory(DjangoModelFactory):
    msg = factory.Faker("name")
    nombre_archivo = factory.Faker("file_name", category="office")
    fecha = factory.Faker("date_object")
    laboratorio = factory.Faker("name")
    ci_pasaporte = factory.Faker("name")
    fecha_toma_muestra = date.today()
    edad = 10
    sexo = "M"
    nombre_apellidos = factory.Faker("name")
    condicion = factory.Faker("name")
    direccion = factory.Faker("name")
    municipio = factory.Faker("name")
    provincia = factory.Faker("name")
    id_provincia = factory.Faker("name")
    pais_procedencia = factory.Faker("name")
    procedencia_entrega = factory.Faker("name")
    area_salud = factory.Faker("name")
    f_inicio_sintomas = factory.Faker("name")
    tipo_muestra = factory.Faker("name")
    fecha_inicio_sintomas = date.today()
    ct = factory.Faker("name")
    fecha_salida = date.today()

    class Meta:
        model = models.DataHigieneError


class DataEpidemiologiaErrorFactory(DjangoModelFactory):
    msg = factory.Faker("name")
    nombre_archivo = factory.Faker("file_name", category="office")
    fecha = factory.Faker("date_object")
    covid_plus = factory.Faker("name")
    no_pcr_realizado = factory.Faker("name")
    laboratorio = factory.Faker("name")
    nombre_apellido = factory.Faker("name")
    ci_pasaporte = factory.Faker("name")
    edad = factory.Faker("name")
    sexo = factory.Faker("name")
    direccion = factory.Faker("name")
    municipio = factory.Faker("name")
    aislamiento = factory.Faker("name")
    fis = factory.Faker("name")
    muestra = factory.Faker("name")
    ftm = factory.Faker("name")
    fecha_envio = factory.Faker("name")
    resultado = factory.Faker("name")
    fecha_resultado = date.today()
    hora = date.today().strftime("%H:%M")
    pcr_contactos_viajeros = date.today()
    condicion = factory.Faker("name")
    pais = factory.Faker("name")
    observaciones = factory.Faker("name")

    class Meta:
        model = models.DataEpidemiologiaError


class PlacaErrorFactory(DjangoModelFactory):
    msg = factory.Faker("name")
    nombre_archivo = factory.Faker("file_name", category="office")
    fecha = factory.Faker("date_object")
    fecha = factory.Faker("name")
    laboratorio = factory.Faker("name")
    no_muestra = factory.Faker("name")
    ci = factory.Faker("name")
    edad = factory.Faker("name")
    sexo = factory.Faker("name")
    nombre_apellidos = factory.Faker("name")
    municipio = factory.Faker("name")
    provincia = factory.Faker("name")
    resultado = factory.Faker("name")
    fecha_resultado = factory.Faker("name")

    class Meta:
        model = models.PlacaErrorModel
