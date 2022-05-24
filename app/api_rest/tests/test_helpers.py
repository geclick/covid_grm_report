from datetime import date
from django.test import TestCase
from rest_framework import serializers

from api_rest import helpers, models
from . import factories


class DiagnoseTest(TestCase):

    def test_alredy_positive_result(self):
        result_date = date(1965, 5, 30)

        with self.settings(POSITIVE_TEST='Positivo'):
            sample = factories.DataEpidemiologiaFactory(
                no_muestra=5, resultado='Positivo')
            with self.assertRaises(serializers.ValidationError):
                helpers.diagnose(
                    sample, resultado='Negativo', fecha_resultado=result_date)

        register = models.ResultRegister.objects.filter(
            sample=sample, result='Negativo', result_date=result_date)

        self.assertFalse(register.exists())

    def test_update_success(self):
        result_date = date(1965, 5, 30)

        with self.settings(POSITIVE_TEST='Positivo'):
            sample = factories.DataEpidemiologiaFactory(
                no_muestra=5, resultado='Negativo')
            helpers.diagnose(
                sample, resultado='Positivo', fecha_resultado=result_date)

        sample = models.DataEpidemiologiaModel.objects.filter(
            no_muestra=5, resultado='Positivo', fecha_resultado=result_date)

        self.assertTrue(sample.exists())
