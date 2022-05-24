import tempfile
from datetime import date
from typing import Any, Sequence

import factory
from factory import DjangoModelFactory, Faker, post_generation

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from api_rest.permissions import get_group_model_permissions
from api_rest import models


class GenericGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    name = factory.Sequence(lambda n: "Group #%s" % n)

    # https://factoryboy.readthedocs.io/en/v2.7.0/recipes.html
    @factory.post_generation
    def permissions(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for permission in extracted:
                self.permissions.add(permission)


class InvitadoGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    name = factory.Sequence(lambda n: "INVITADO #%s" % n)

    @factory.post_generation
    def permissions(self, create, extracted, **kwargs):
        for permission in get_group_model_permissions("INVITADO"):
            self.permissions.add(permission)


class CentroGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    name = factory.Sequence(lambda n: "CENTRO #%s" % n)

    @factory.post_generation
    def permissions(self, create, extracted, **kwargs):
        for permission in get_group_model_permissions("CENTRO"):
            self.permissions.add(permission)


class CapturadorGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    name = factory.Sequence(lambda n: "CAPTURADOR #%s" % n)

    @factory.post_generation
    def permissions(self, create, extracted, **kwargs):
        for permission in get_group_model_permissions("CAPTURADOR"):
            self.permissions.add(permission)


class SupervisorGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    name = factory.Sequence(lambda n: "SUPERVISOR #%s" % n)

    @factory.post_generation
    def permissions(self, create, extracted, **kwargs):
        for permission in get_group_model_permissions("SUPERVISOR"):
            self.permissions.add(permission)


class UserFactory(DjangoModelFactory):

    username = Faker("user_name")
    email = Faker("email")

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = (
            extracted
            if extracted
            else Faker(
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).generate(extra_kwargs={})
        )
        self.set_password(password)

    # https://factoryboy.readthedocs.io/en/v2.7.0/recipes.html
    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for group in extracted:
                self.groups.add(group)

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]


class LaboratorioFactory(DjangoModelFactory):
    nombre = factory.Faker("name")

    class Meta:
        model = models.Laboratorio


class ResultFactory(DjangoModelFactory):
    laboratorio = factory.SubFactory(LaboratorioFactory)
    lab_procesado = factory.SubFactory(LaboratorioFactory)
    archivo = factory.django.FileField(from_file=tempfile.NamedTemporaryFile())

    class Meta:
        model = models.ResultModel


class DataHigieneFactory(DjangoModelFactory):
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
    resultado = factory.Faker("name")
    fecha_inicio_sintomas = date.today()
    ct = factory.Faker("name")
    fecha_salida = date.today()

    class Meta:
        model = models.DataHigieneModel


class DataEpidemiologiaFactory(DjangoModelFactory):
    laboratorio = factory.Faker("name")
    nombre_apellido = factory.Faker("name")
    ci_pasaporte = factory.Faker("name")
    edad = 50
    sexo = "M"
    direccion = factory.Faker("name")
    municipio = factory.Faker("name")
    aislamiento = factory.Faker("name")
    fis = factory.Faker("name")
    muestra = factory.Faker("name")
    ftm = date.today()
    fecha_envio = date.today()
    resultado = ""
    fecha_resultado = date.today()
    pcr_contactos_viajeros = date.today()
    condicion = factory.Faker("name")
    pais = factory.Faker("name")
    observaciones = factory.Faker("name")

    class Meta:
        model = models.DataEpidemiologiaModel


class TestResultFactory(DjangoModelFactory):
    nombre = factory.Faker("name")

    class Meta:
        model = models.TestResult


class EpidemiologiaUploadFactory(DjangoModelFactory):
    archivo = factory.django.FileField(from_file=tempfile.NamedTemporaryFile())

    class Meta:
        model = models.EpidemiologiaUploadModel


class HigieneUploadFactory(DjangoModelFactory):
    archivo = factory.django.FileField(from_file=tempfile.NamedTemporaryFile())
    laboratorio = factory.SubFactory(LaboratorioFactory)

    class Meta:
        model = models.HigieneUploadModel
