import tempfile

from openpyxl import load_workbook
from django.test import TestCase
from rest_framework.test import APIClient

from . import factories
from api_rest import models


client = APIClient()


class TestViewsXLSBase(TestCase):
    """Base Tests for the Views"""

    def setUp(self):
        # test for Capturadores
        group = factories.CapturadorGroupFactory()
        user = factories.UserFactory(groups=[group])
        client.force_authenticate(user=user)

        response = client.post(
            "/api/v1/epidemiologia/",
            {
                "covid_plus": 3,
                "no_pcr_realizado": 55,
                "no_muestra": 3,
                "laboratorio": "HOLGUIN",
                "nombre_apellido": "Yisel de los Ángeles",
                "ci_pasaporte": "55312547",
                "edad": 45,
                "sexo": "F",
                "direccion": "Calle 31",
                "municipio": "Bayamo",
                "aislamiento": "Hosp. Gelacio Calaña",
                "fis": "FIEBRE,TOS,EXPECTORACION,RINORREA",
                "muestra": "Covid-19",
                "ftm": "2021-03-19",
                "fecha_envio": "2021-03-19",
                "resultado": "Positivo",
                "fecha_resultado": "2021-03-19",
                "hora": "00:00:00",
                "pcr_contactos_viajeros": "Si",
                "condicion": "Activo",
                "pais": "Cuba",
                "observaciones": "Estable",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        assert models.DataEpidemiologiaModel.objects.count() == 1

        # test for supervisores
        client.logout()
        group = factories.SupervisorGroupFactory()
        user = factories.UserFactory(groups=[group])
        client.force_authenticate(user=user)

        response = client.post(
            "/api/v1/epidemiologia/",
            {
                "covid_plus": 3,
                "no_pcr_realizado": 55,
                "no_muestra": 789,
                "laboratorio": "HOLGUIN",
                "nombre_apellido": "Yisel de los Ángeles",
                "ci_pasaporte": "55312547",
                "edad": 45,
                "sexo": "F",
                "direccion": "Calle 31",
                "municipio": "Bayamo",
                "aislamiento": "Hosp. Gelacio Calaña",
                "fis": "FIEBRE,TOS,EXPECTORACION,RINORREA",
                "muestra": "Covid-19",
                "ftm": "2021-03-19",
                "fecha_envio": "2021-03-19",
                "resultado": "Positivo",
                "fecha_resultado": "2021-03-19",
                "hora": "00:00:00",
                "pcr_contactos_viajeros": "Si",
                "condicion": "Activo",
                "pais": "Cuba",
                "observaciones": "Estable",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        assert models.DataEpidemiologiaModel.objects.count() == 2


class TestViewsXLSGeneral(TestViewsXLSBase):
    """General Tests"""

    def test_success(self):
        response = client.get("/api/v1/epidemiologia/xlsx")
        self.assertEqual(response.status_code, 200)

        with self.settings(MEDIA_ROOT=tempfile.gettempdir()):
            xls_file = tempfile.NamedTemporaryFile(suffix=".xlsx")
            xls_file.write(response.content)
            xls_file.seek(0)
            wb = load_workbook(filename=xls_file.name)

        self.assertIn("Report", wb)
        sheet = wb["Report"]

        # Field names
        self.assertEquals("Covid+", sheet["A1"].value)
        self.assertEquals("No PCR Realizado", sheet["B1"].value)
        self.assertEquals("No Muestra", sheet["C1"].value)
        self.assertEquals("Laboratorio", sheet["D1"].value)
        self.assertEquals("Nombres y Apellidos", sheet["E1"].value)
        self.assertEquals("Edad", sheet["F1"].value)
        self.assertEquals("Sexo", sheet["G1"].value)
        self.assertEquals("Dirección", sheet["H1"].value)
        self.assertEquals("Municipio", sheet["I1"].value)
        self.assertEquals("Aislamiento", sheet["J1"].value)
        self.assertEquals("FIS", sheet["K1"].value)
        self.assertEquals("FTM", sheet["L1"].value)
        self.assertEquals("Muestra", sheet["M1"].value)
        self.assertEquals("Fecha envío", sheet["N1"].value)
        self.assertEquals("Resultados", sheet["O1"].value)
        self.assertEquals("Fecha resultado", sheet["P1"].value)
        self.assertEquals("Hora resultado", sheet["Q1"].value)
        self.assertEquals("PCR de los Contactos y Viajeros", sheet["R1"].value)
        self.assertEquals("Condición", sheet["S1"].value)
        self.assertEquals("País", sheet["T1"].value)
        self.assertEquals("Observación", sheet["U1"].value)

        # Field data
        self.assertEquals(3, sheet["A2"].value)
        self.assertEquals(55, sheet["B2"].value)
        self.assertEquals(3, sheet["C2"].value)
        self.assertEquals("HOLGUIN", sheet["D2"].value)
        self.assertEquals("Yisel de los Ángeles", sheet["E2"].value)
        self.assertEquals(45, sheet["F2"].value)
        self.assertEquals("F", sheet["G2"].value)
        self.assertEquals("Calle 31", sheet["H2"].value)
        self.assertEquals("Bayamo", sheet["I2"].value)
        self.assertEquals("Hosp. Gelacio Calaña", sheet["J2"].value)
        self.assertEquals(
            "FIEBRE,TOS,EXPECTORACION,RINORREA", sheet["K2"].value
        )
        self.assertEquals("2021-03-19", sheet["L2"].value)
        self.assertEquals("Covid-19", sheet["M2"].value)
        self.assertEquals("2021-03-19", sheet["N2"].value)
        self.assertEquals("Positivo", sheet["O2"].value)
        self.assertEquals("2021-03-19", sheet["P2"].value)
        self.assertEquals("00:00:00", sheet["Q2"].value)
        self.assertEquals("Si", sheet["R2"].value)
        self.assertEquals("Activo", sheet["S2"].value)
        self.assertEquals("Cuba", sheet["T2"].value)
        self.assertEquals("Estable", sheet["U2"].value)
