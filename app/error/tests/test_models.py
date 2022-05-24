from django.test import TestCase

from . import factories


class DataHigieneErrorTest(TestCase):
    def test_archivo_url(self):
        data = factories.DataHigieneErrorFactory()

        with self.settings(
            PROTECTED_MEDIA_ROOT="/tmp",
            HIGIENE_DIR_PROCESSED="higie/processed/",
        ):
            expected = f"/tmp/higie/processed/{data.nombre_archivo}"
            self.assertEqual(data.archivo, expected)


class DataEpidemiologiaErrorTest(TestCase):
    def test_archivo_url(self):
        data = factories.DataEpidemiologiaErrorFactory()

        with self.settings(
            PROTECTED_MEDIA_ROOT="/tmp",
            EPIDEMIOLOGIA_DIR_PROCESSED="epi/processed/",
        ):
            expected = f"/tmp/epi/processed/{data.nombre_archivo}"
            self.assertEqual(data.archivo, expected)


class PlacaErrorTest(TestCase):
    def test_archivo_url(self):
        data = factories.PlacaErrorFactory()

        with self.settings(
            PROTECTED_MEDIA_ROOT="/tmp", LAB_DIR_PROCESSED="lab/processed/"
        ):
            expected = f"/tmp/lab/processed/{data.nombre_archivo}"
            self.assertEqual(data.archivo, expected)
