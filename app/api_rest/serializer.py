from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from api_rest.mixins import NestedCreateMixin, NestedUpdateMixin
from api_rest.models import DataHigieneModel, DataEpidemiologiaModel

from . import models


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "is_staff",
            "is_active",
            "is_superuser",
        )
        # fields = ('__all__')
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(
            email=validated_data["email"], username=validated_data["username"]
        )
        user.set_password(validated_data["password"])
        user.save()
        Token.objects.create(user=user)
        return user


class WritableNestedModelSerializer(
    NestedCreateMixin, NestedUpdateMixin, serializers.ModelSerializer
):
    pass


class DataHigieneSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataHigieneModel
        fields = (
            "laboratorio",
            "fecha_envio",
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


class DataEpidemiologiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataEpidemiologiaModel
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


class DataEpidemiologiaColorRowSerializer(DataEpidemiologiaSerializer):

    row_color = serializers.CharField(default="FFFFFF")

    class Meta(DataEpidemiologiaSerializer.Meta):
        fields = DataEpidemiologiaSerializer.Meta.fields + ("row_color",)

    def to_representation(self, instance):
        representation = super(
            DataEpidemiologiaColorRowSerializer, self
        ).to_representation(instance)
        if instance.resultado and (
            settings.POSITIVE_TEST in instance.resultado
        ):
            representation["row_color"] = "FF0000"
        return representation


class DataLaboratorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DataEpidemiologiaModel
        fields = ["resultado", "fecha_resultado", "hora"]
        extra_kwargs = {
            "resultado": {"required": True},
            "fecha_resultado": {"required": True},
            "hora": {"required": False},
        }

    def validate_resultado(self, value):
        if self.instance.resultado == settings.POSITIVE_TEST:
            detail = "La muestra ya fue diagnosticada como positiva"
            raise serializers.ValidationError(detail, code="diagnosed")

        return value


class ResultRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ResultRegister
        fields = [
            "sample",
            "result",
            "result_date",
            "new_result",
            "new_result_date",
        ]


class MunicipioSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Municipio
        fields = "__all__"
