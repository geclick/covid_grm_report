'''Test for utils module'''
import tempfile
from datetime import date

from django.test import TestCase

from api_rest import models
from . import factories


class HigieneUploadModelTest(TestCase):
    def test_str(self):
        with self.settings(MEDIA_ROOT=tempfile.gettempdir()):
            instance = factories.ResultFactory(fecha=date(1985, 5, 30))
            lab = instance.laboratorio.nombre
            lab_procesado = instance.lab_procesado.nombre

        self.assertEqual(str(instance), f'{lab}-1985-05-30-{lab_procesado}')


class DataHigieneModelTest(TestCase):
    def test_ordering(self):
        factories.DataHigieneFactory.create(codigo=1)
        factories.DataHigieneFactory.create(codigo=2)

        data = models.DataHigieneModel.objects.last()
        self.assertEqual(data.codigo, 2)

    def test_create_epidemiologia(self):
        factories.DataHigieneFactory.create(codigo=3)

        data = models.DataEpidemiologiaModel.objects.last()
        self.assertEqual(data.no_muestra, 3)

    def test_update_epidemiologia(self):
        higiene = factories.DataHigieneFactory.create(codigo=4)
        higiene.codigo = 456
        higiene.save()

        data = models.DataEpidemiologiaModel.objects.last()
        self.assertEqual(data.no_muestra, 456)


class DataEpidemiologiaModelTest(TestCase):
    def test_ordering(self):
        factories.DataEpidemiologiaFactory.create(no_muestra=1)
        factories.DataEpidemiologiaFactory.create(no_muestra=2)

        data = models.DataEpidemiologiaModel.objects.last()
        self.assertEqual(data.no_muestra, 2)


class AutoDataEpidemiologiaTest(TestCase):
    '''
    Test auto-generation of fields no_pcr_realizado and covid_plus
    '''

    def test_no_records(self):
        factories.DataHigieneFactory(codigo=45)
        data = models.DataEpidemiologiaModel.objects.first()

        self.assertEqual(data.no_pcr_realizado, 1)
        self.assertEqual(data.covid_plus, 1)

    def test_with_one_record(self):
        factories.DataEpidemiologiaFactory(
            no_muestra=45,
            no_pcr_realizado=250,
            covid_plus=50
        )
        factories.DataHigieneFactory(codigo=46)
        data = models.DataEpidemiologiaModel.objects.last()

        self.assertEqual(data.no_pcr_realizado, 251)
        self.assertEqual(data.covid_plus, 51)

    def test_with_multiple_records(self):
        factories.DataEpidemiologiaFactory(
            no_muestra=45,
            no_pcr_realizado=250,
            covid_plus=50
        )
        factories.DataEpidemiologiaFactory(
            no_muestra=46,
            no_pcr_realizado=251,
            covid_plus=51
        )
        factories.DataHigieneFactory(codigo=47)
        data = models.DataEpidemiologiaModel.objects.last()

        self.assertEqual(data.no_pcr_realizado, 252)
        self.assertEqual(data.covid_plus, 52)

    def test_with_covid_reset(self):
        factories.DataEpidemiologiaFactory(
            no_muestra=45,
            no_pcr_realizado=250,
            covid_plus=50
        )
        factories.DataEpidemiologiaFactory(
            no_muestra=46,
            no_pcr_realizado=251,
            covid_plus=10
        )
        factories.DataHigieneFactory(codigo=47)
        data = models.DataEpidemiologiaModel.objects.last()

        self.assertEqual(data.no_pcr_realizado, 252)
        self.assertEqual(data.covid_plus, 11)

    def test_last_no_pcr_null(self):
        factories.DataEpidemiologiaFactory(
            no_muestra=45,
            no_pcr_realizado=250,
            covid_plus=50
        )
        factories.DataEpidemiologiaFactory(
            no_muestra=46,
            no_pcr_realizado=None,
            covid_plus=10
        )
        factories.DataHigieneFactory(codigo=47)
        data = models.DataEpidemiologiaModel.objects.last()

        self.assertEqual(data.no_pcr_realizado, 251)
        self.assertEqual(data.covid_plus, 51)

    def test_records_without_no_pcr(self):
        factories.DataEpidemiologiaFactory(
            no_muestra=45,
            no_pcr_realizado=250,
            covid_plus=50
        )
        factories.DataEpidemiologiaFactory(
            no_muestra=46,
            no_pcr_realizado=None,
            covid_plus=10
        )
        factories.DataEpidemiologiaFactory(
            no_muestra=47,
            no_pcr_realizado=251,
            covid_plus=51
        )
        factories.DataHigieneFactory(codigo=48)
        data = models.DataEpidemiologiaModel.objects.last()

        self.assertEqual(data.no_pcr_realizado, 252)
        self.assertEqual(data.covid_plus, 52)

    def test_records_without_covid_plus(self):
        factories.DataEpidemiologiaFactory(
            no_muestra=45,
            no_pcr_realizado=250,
            covid_plus=None
        )
        factories.DataHigieneFactory(codigo=46)
        data = models.DataEpidemiologiaModel.objects.last()

        self.assertEqual(data.no_pcr_realizado, 251)
