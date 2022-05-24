"""Test for utils module"""
import unittest
import tempfile
import time_machine
from datetime import date

from django.test import TestCase

from api_rest import utils
from api_rest import models
from . import factories


class LabDirectoryTest(TestCase):
    @unittest.skip("Problem with date mocking")
    def test_path(self):
        tempdir = tempfile.gettempdir()
        timestamp = "1615179600_0"

        with self.settings(MEDIA_ROOT=tempdir, LAB_DIR="shared/lab/"):
            instance = factories.ResultFactory(fecha=date(1985, 5, 30))
            lab = instance.laboratorio.nombre.upper()
            lab_procesado = instance.lab_procesado.nombre.upper()

            with time_machine.travel(date(2021, 3, 8)):
                path = utils.lab_directory_path(instance, "pepe.xls")

            expected = f"shared/lab/{lab}-30051985-{lab_procesado}_{timestamp}"
            self.assertEqual(path, expected)


class EpidemiologiaUploadTest(TestCase):
    @unittest.skip("Problem with date mocking")
    def test_path(self):
        tempdir = tempfile.gettempdir()
        timestamp = "1615179600_0"

        with self.settings(MEDIA_ROOT=tempdir, EPIDEMIOLOGIA_DIR="shared/bd/"):
            instance = factories.EpidemiologiaUploadFactory(
                fecha=date(1985, 5, 30)
            )

            with time_machine.travel(date(2021, 3, 8)):
                path = utils.epidemiologia_directory_path(instance, "pepe.xls")

            expected = f"shared/bd/bd-30051985_{timestamp}"
            self.assertEqual(path, expected)


class HigieneUploadTest(TestCase):
    @unittest.skip("Problem with date mocking")
    def test_path(self):
        tempdir = tempfile.gettempdir()
        timestamp = "1615179600_0"

        with self.settings(MEDIA_ROOT=tempdir, LAB_DIR="shared/higie/"):
            instance = factories.HigieneUploadFactory(fecha=date(1985, 5, 30))
            lab = instance.laboratorio.nombre.upper()

            with time_machine.travel(date(2021, 3, 8)):
                path = utils.higiene_directory_path(instance, "pepe.xls")

            expected = f"shared/higie/{lab}-30051985_{timestamp}"
            self.assertEqual(path, expected)


class TestResultMatch(TestCase):
    def test_match(self):
        models.TestResult.objects.create(nombre="pendiente")
        models.TestResult.objects.create(nombre="positivo")
        models.TestResult.objects.create(nombre="negativo")
        models.TestResult.objects.create(nombre="dudoso")
        models.TestResult.objects.create(nombre="contaminada")

        self.assertEqual(utils.match_test_result("Pendiente"), "PENDIENTE")
        self.assertEqual(utils.match_test_result("PENDIENTE"), "PENDIENTE")
        self.assertEqual(utils.match_test_result("pendente"), "PENDIENTE")
        self.assertEqual(utils.match_test_result("pendentes"), "PENDIENTE")
        self.assertEqual(utils.match_test_result("endiéntes"), "PENDIENTE")
        self.assertEqual(utils.match_test_result("pendienta"), "PENDIENTE")

    def test_non_posibles_result(self):

        self.assertEqual(utils.match_test_result("Pendiente"), "PENDIENTE")
