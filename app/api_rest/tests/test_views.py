import time
from datetime import date, timedelta
from collections import ChainMap


from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from . import factories
from api_rest import models

from django.conf import settings


client = APIClient()


class TokenExpirationTest(TestCase):
    def test_token_expiration(self):
        client.logout()

        group = factories.InvitadoGroupFactory()
        user = factories.UserFactory(groups=[group])
        user.set_password("prueba")
        user.save()

        with override_settings(
            JWT_AUTH=ChainMap(
                settings.JWT_AUTH,
                {"JWT_EXPIRATION_DELTA": timedelta(seconds=10)},
            )
        ):

            response = client.post(
                "/api/v1/session/obtain_token/",
                {"password": "prueba", "username": user.username},
                format="json",
            )

            self.assertEqual(response.status_code, 201)
            self.assertTrue("token" in response.json())

            token = response.json()["token"]

            client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

            response = client.get("/api/v1/higiene/")

            self.assertEqual(response.status_code, 200)

            time.sleep(11)

            response = client.get("/api/v1/higiene/")

            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json(), {"detail": "Token has expired."})

    def test_token_expiration_root(self):
        user = factories.UserFactory(is_superuser=True)
        user.set_password("prueba")
        user.save()

        with override_settings(
            JWT_AUTH=ChainMap(
                settings.JWT_AUTH,
                {"JWT_EXPIRATION_DELTA": timedelta(seconds=10)},
            )
        ):

            response = client.post(
                "/api/v1/session/obtain_token/",
                {"username": user.username, "password": "prueba"},
                format="json",
            )

            self.assertEqual(response.status_code, 201)
            self.assertTrue("token" in response.json())

            token = response.json()["token"]

            client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

            response = client.get("/api/v1/epidemiologia-errores/")

            self.assertEqual(response.status_code, 200)

            time.sleep(11)

            response = client.get("/api/v1/epidemiologia-errores/")

            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json(), {"detail": "Token has expired."})


class HigieneListTest(TestCase):
    def test_no_login(self):
        client.logout()
        response = client.get("/api/v1/higiene/")

        self.assertEqual(response.status_code, 401)

    def test_no_permission(self):
        user = factories.UserFactory()
        client.force_authenticate(user=user)

        response = client.get("/api/v1/higiene/")

        self.assertEqual(response.status_code, 403)

    def test_invitado_succes(self):
        group = factories.InvitadoGroupFactory()
        user = factories.UserFactory(groups=[group])
        client.force_authenticate(user=user)

        factories.DataHigieneFactory(codigo=5645)

        response = client.get("/api/v1/higiene/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 1)

    def test_supervisor_succes(self):
        group = factories.SupervisorGroupFactory()
        user = factories.UserFactory(groups=[group])
        client.force_authenticate(user=user)

        factories.DataHigieneFactory(codigo=5645)

        response = client.get("/api/v1/higiene/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 1)


class HigieneCreateTest(TestCase):
    def test_no_permission(self):
        user = factories.UserFactory()
        client.force_authenticate(user=user)
        response = client.post("/api/v1/higiene/", {}, format="json")
        self.assertEqual(response.status_code, 403)

    def test_success_capturador(self):
        group = factories.CapturadorGroupFactory()
        user = factories.UserFactory(groups=[group])
        client.force_authenticate(user=user)

        response = client.post(
            "/api/v1/higiene/",
            {
                "codigo": 3,
                "ci_pasaporte": "55312547",
                "edad": 32,
                "sexo": "M",
                "nombre_apellidos": "Yisel de los Ángeles",
                "condicion": "Grave",
                "direccion": "Calle 31",
                "laboratorio": "HOLGUIN",
                "municipio": "Bayamo",
                "provincia": "Granma",
                "id_provincia": "Granma",
                "pais_procedencia": "Cuba",
                "area_salud": "13 de marzo",
                "observaciones": "",
                "ct": "Fiebre",
                "tipo_muestra": "variado",
                "fecha_salida": "2020-03-03",
                "fecha_envio": "2020-03-03",
                "f_inicio_sintoma": "2020-03-03",
                "fecha_inicio_sintomas": "2020-03-03",
                "fecha_toma_muestra": "2020-03-03",
                "procedencia_entrega": "salud",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        assert models.DataHigieneModel.objects.count() == 1
        assert models.DataEpidemiologiaModel.objects.count() == 1
        exists = models.DataHigieneModel.objects.filter(codigo="03").exists()
        epi = models.DataEpidemiologiaModel.objects.get(no_muestra="03")

        self.assertTrue(exists)
        self.assertEqual(epi.no_pcr_realizado, 1)
        self.assertEqual(epi.covid_plus, 1)

    def test_success_supervisor(self):
        group = factories.SupervisorGroupFactory()
        user = factories.UserFactory(groups=[group])
        client.force_authenticate(user=user)

        response = client.post(
            "/api/v1/higiene/",
            {
                "codigo": 3,
                "ci_pasaporte": "55312547",
                "edad": 32,
                "sexo": "M",
                "nombre_apellidos": "Yisel de los Ángeles",
                "condicion": "Grave",
                "direccion": "Calle 31",
                "laboratorio": "HOLGUIN",
                "municipio": "Bayamo",
                "provincia": "Granma",
                "id_provincia": "Granma",
                "pais_procedencia": "Cuba",
                "area_salud": "13 de marzo",
                "observaciones": "",
                "ct": "Fiebre",
                "tipo_muestra": "variado",
                "fecha_salida": "2020-03-03",
                "fecha_envio": "2020-03-03",
                "f_inicio_sintoma": "2020-03-03",
                "fecha_inicio_sintomas": "2020-03-03",
                "fecha_toma_muestra": "2020-03-03",
                "procedencia_entrega": "salud",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        assert models.DataHigieneModel.objects.count() == 1
        assert models.DataEpidemiologiaModel.objects.count() == 1
        exists = models.DataHigieneModel.objects.filter(codigo="03").exists()
        epi = models.DataEpidemiologiaModel.objects.get(no_muestra="03")

        self.assertTrue(exists)
        self.assertEqual(epi.no_pcr_realizado, 1)
        self.assertEqual(epi.covid_plus, 1)

    def test_register_already_exist_capturador(self):
        group = factories.CapturadorGroupFactory()
        user = factories.UserFactory(groups=[group])
        client.force_authenticate(user=user)

        factories.DataHigieneFactory(codigo=3)

        response = client.post(
            "/api/v1/higiene/",
            {
                "codigo": 3,
                "ci_pasaporte": "55312547",
                "edad": 32,
                "sexo": "M",
                "nombre_apellidos": "Yisel de los Ángeles",
                "condicion": "Grave",
                "direccion": "Calle 31",
                "laboratorio": "HOLGUIN",
                "municipio": "Bayamo",
                "provincia": "Granma",
                "id_provincia": "Granma",
                "pais_procedencia": "Cuba",
                "area_salud": "13 de marzo",
                "observaciones": "",
                "ct": "Fiebre",
                "tipo_muestra": "variado",
                "fecha_salida": "2020-03-03",
                "fecha_envio": "2020-03-03",
                "f_inicio_sintoma": "2020-03-03",
                "fecha_inicio_sintomas": "2020-03-03",
                "fecha_toma_muestra": "2020-03-03",
                "procedencia_entrega": "salud",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("codigo", response.data)

    def test_register_already_exist_supervisor(self):
        group = factories.SupervisorGroupFactory()
        user = factories.UserFactory(groups=[group])
        client.force_authenticate(user=user)

        factories.DataHigieneFactory(codigo=3)

        response = client.post(
            "/api/v1/higiene/",
            {
                "codigo": 3,
                "ci_pasaporte": "55312547",
                "edad": 32,
                "sexo": "M",
                "nombre_apellidos": "Yisel de los Ángeles",
                "condicion": "Grave",
                "direccion": "Calle 31",
                "laboratorio": "HOLGUIN",
                "municipio": "Bayamo",
                "provincia": "Granma",
                "id_provincia": "Granma",
                "pais_procedencia": "Cuba",
                "area_salud": "13 de marzo",
                "observaciones": "",
                "ct": "Fiebre",
                "tipo_muestra": "variado",
                "fecha_salida": "2020-03-03",
                "fecha_envio": "2020-03-03",
                "f_inicio_sintoma": "2020-03-03",
                "fecha_inicio_sintomas": "2020-03-03",
                "fecha_toma_muestra": "2020-03-03",
                "procedencia_entrega": "salud",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("codigo", response.data)


class HigieneUpdateTest(TestCase):
    def test_no_permission(self):
        user = factories.UserFactory()
        client.force_authenticate(user=user)

        response = client.put("/api/v1/higiene/", {}, format="json")
        self.assertEqual(response.status_code, 403)

    def test_record_not_found_supervisor(self):
        group = factories.SupervisorGroupFactory()
        user = factories.UserFactory(groups=[group])
        client.force_authenticate(user=user)

        response = client.put(
            "/api/v1/higiene/3/",
            {
                "codigo": 3,
                "nombre_apellidos": "Yisel de los Ángeles",
                "laboratorio": "HOLGUIN",
                "municipio": "Bayamo",
                "provincia": "Granma",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 404)

    def test_success_supervisor(self):
        group = factories.SupervisorGroupFactory()
        user = factories.UserFactory(groups=[group])
        client.force_authenticate(user=user)

        factories.DataHigieneFactory(codigo=3)

        response = client.put(
            "/api/v1/higiene/3/",
            {
                "codigo": 3,
                "nombre_apellidos": "Yisel de los Ángeles",
                "laboratorio": "HOLGUIN",
                "municipio": "Bayamo",
                "provincia": "Granma",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)


class EpidemiologiaListTest(TestCase):
    def test_no_login(self):
        client.logout()
        response = client.get("/api/v1/epidemiologia/")

        self.assertEqual(response.status_code, 401)

    def test_no_permission(self):
        user = factories.UserFactory()
        client.force_authenticate(user=user)

        response = client.get("/api/v1/epidemiologia/")

        self.assertEqual(response.status_code, 403)

    def test_success_centro(self):
        group = factories.CentroGroupFactory()
        user = factories.UserFactory(groups=[group])
        client.force_authenticate(user=user)

        factories.DataHigieneFactory(codigo=5646)

        response = client.get("/api/v1/epidemiologia/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 1)

    def test_success_invitado(self):
        group = factories.InvitadoGroupFactory()
        user = factories.UserFactory(groups=[group])
        client.force_authenticate(user=user)

        factories.DataHigieneFactory(codigo=5646)

        response = client.get("/api/v1/epidemiologia/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 1)

    def test_success_capturador(self):
        group = factories.CapturadorGroupFactory()
        user = factories.UserFactory(groups=[group])
        client.force_authenticate(user=user)

        factories.DataHigieneFactory(codigo=5646)

        response = client.get("/api/v1/epidemiologia/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 1)

    def test_success_supervisor(self):
        group = factories.SupervisorGroupFactory()
        user = factories.UserFactory(groups=[group])
        client.force_authenticate(user=user)

        factories.DataHigieneFactory(codigo=5646)

        response = client.get("/api/v1/epidemiologia/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 1)


class EpidemiologiaUpsertTest(TestCase):
    def test_create_supervisor(self):
        group = factories.SupervisorGroupFactory()
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
                "sexo": "M",
                "direccion": "Calle 31",
                "municipio": "Bayamo",
                "aislamiento": "Grave",
                "fis": "Fiebre",
                "muestra": "variado",
                "ftm": "2020-03-03",
                "fecha_envio": "2020-03-03",
                "resultado": "salud",
                "fecha_resultado": "2020-03-03",
                "pcr_contactos_viajeros": "2020-03-03",
                "condicion": "13 de marzo",
                "pais": "Cuba",
                "observaciones": "",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        assert models.DataEpidemiologiaModel.objects.count() == 1
        exists = models.DataEpidemiologiaModel.objects.filter(
            no_muestra="3"
        ).exists()

        self.assertTrue(exists)

    def test_create_capturador(self):
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
                "sexo": "M",
                "direccion": "Calle 31",
                "municipio": "Bayamo",
                "aislamiento": "Grave",
                "fis": "Fiebre",
                "muestra": "variado",
                "ftm": "2020-03-03",
                "fecha_envio": "2020-03-03",
                "resultado": "salud",
                "fecha_resultado": "2020-03-03",
                "pcr_contactos_viajeros": "2020-03-03",
                "condicion": "13 de marzo",
                "pais": "Cuba",
                "observaciones": "",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        assert models.DataEpidemiologiaModel.objects.count() == 1
        exists = models.DataEpidemiologiaModel.objects.filter(
            no_muestra="3"
        ).exists()

        self.assertTrue(exists)

    def test_without_no_muestra_supervisor(self):
        group = factories.SupervisorGroupFactory()
        user = factories.UserFactory(groups=[group])
        client.force_authenticate(user=user)

        response = client.post(
            "/api/v1/epidemiologia/",
            {
                "laboratorio": "HOLGUIN",
                "nombre_apellido": "Yisel de los Ángeles",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("no_muestra", response.data)

    def test_without_no_muestra_capturador(self):
        group = factories.CapturadorGroupFactory()
        user = factories.UserFactory(groups=[group])
        client.force_authenticate(user=user)

        response = client.post(
            "/api/v1/epidemiologia/",
            {
                "laboratorio": "HOLGUIN",
                "nombre_apellido": "Yisel de los Ángeles",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("no_muestra", response.data)

    def test_update_supervisor(self):
        group = factories.SupervisorGroupFactory()
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
                "sexo": "M",
                "direccion": "Calle 31",
                "municipio": "Bayamo",
                "aislamiento": "Grave",
                "fis": "Fiebre",
                "muestra": "variado",
                "ftm": "2020-03-03",
                "fecha_envio": "2020-03-03",
                "resultado": "",
                "fecha_resultado": "2020-03-03",
                "pcr_contactos_viajeros": "2020-03-03",
                "condicion": "13 de marzo",
                "pais": "Cuba",
                "observaciones": "",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        assert models.DataEpidemiologiaModel.objects.count() == 1

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
                "sexo": "M",
                "direccion": "Calle 31",
                "municipio": "Bayamo",
                "aislamiento": "Grave",
                "fis": "Fiebre",
                "muestra": "variado",
                "ftm": "2020-03-03",
                "fecha_envio": "2020-03-03",
                "resultado": "Positivo",
                "fecha_resultado": "2020-03-03",
                "pcr_contactos_viajeros": "2020-03-03",
                "condicion": "13 de marzo",
                "pais": "Cuba",
                "observaciones": "",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        assert models.DataEpidemiologiaModel.objects.count() == 1

        object = models.DataEpidemiologiaModel.objects.get(no_muestra="3")
        self.assertEqual(object.resultado, "Positivo")

    def test_update_capturador(self):
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
                "sexo": "M",
                "direccion": "Calle 31",
                "municipio": "Bayamo",
                "aislamiento": "Grave",
                "fis": "Fiebre",
                "muestra": "variado",
                "ftm": "2020-03-03",
                "fecha_envio": "2020-03-03",
                "resultado": "",
                "fecha_resultado": "2020-03-03",
                "pcr_contactos_viajeros": "2020-03-03",
                "condicion": "13 de marzo",
                "pais": "Cuba",
                "observaciones": "",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        assert models.DataEpidemiologiaModel.objects.count() == 1

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
                "sexo": "M",
                "direccion": "Calle 31",
                "municipio": "Bayamo",
                "aislamiento": "Grave",
                "fis": "Fiebre",
                "muestra": "variado",
                "ftm": "2020-03-03",
                "fecha_envio": "2020-03-03",
                "resultado": "Positivo",
                "fecha_resultado": "2020-03-03",
                "pcr_contactos_viajeros": "2020-03-03",
                "condicion": "13 de marzo",
                "pais": "Cuba",
                "observaciones": "",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        assert models.DataEpidemiologiaModel.objects.count() == 1

        object = models.DataEpidemiologiaModel.objects.get(no_muestra="3")
        self.assertEqual(object.resultado, "Positivo")


class UpdateResultTest(TestCase):
    def test_no_entry_in_higiene_capturador(self):
        group = factories.CapturadorGroupFactory()
        user = factories.UserFactory(groups=[group])
        client.force_authenticate(user=user)

        response = client.post(
            "/api/v1/placa/",
            {
                "nombre_apellidos": "Yisel de los Ángeles",
                "laboratorio": "Holgun",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            str(response.data["detail"]),
            "La muestra no esta registrada en la base de datos, verifique!!!",
        )

    def test_no_entry_in_higiene_supervisor(self):
        group = factories.SupervisorGroupFactory()
        user = factories.UserFactory(groups=[group])
        client.force_authenticate(user=user)

        response = client.post(
            "/api/v1/placa/",
            {
                "nombre_apellidos": "Yisel de los Ángeles",
                "laboratorio": "Holgun",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            str(response.data["detail"]),
            "La muestra no esta registrada en la base de datos, verifique!!!",
        )

    def test_no_entry_in_epidemiologia_capturador(self):
        group = factories.CapturadorGroupFactory()
        user = factories.UserFactory(groups=[group])
        client.force_authenticate(user=user)

        factories.DataHigieneFactory(
            codigo=1,
            nombre_apellidos="Yisel de los Ángeles",
            laboratorio="Holguín",
            municipio="Bayamo",
        )

        response = client.post(
            "/api/v1/placa/",
            {
                "nombre_apellidos": "Yisel de los Ángeles",
                "laboratorio": "Holguín",
                "resultado": "POSITIVO",
                "fecha_resultado": "1953-05-03",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)

    def test_no_entry_in_epidemiologia_supervisor(self):
        group = factories.SupervisorGroupFactory()
        user = factories.UserFactory(groups=[group])
        client.force_authenticate(user=user)

        factories.DataHigieneFactory(
            codigo=1,
            nombre_apellidos="Yisel de los Ángeles",
            laboratorio="Holguín",
            municipio="Bayamo",
        )

        response = client.post(
            "/api/v1/placa/",
            {
                "nombre_apellidos": "Yisel de los Ángeles",
                "laboratorio": "Holguín",
                "resultado": "POSITIVO",
                "fecha_resultado": "1953-05-03",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)

    def test_entry_processed_capturador(self):
        group = factories.CapturadorGroupFactory()
        user = factories.UserFactory(groups=[group])
        client.force_authenticate(user=user)

        models.TestResult.objects.create(nombre="positivo")
        models.TestResult.objects.create(nombre="pendiente")

        factories.DataHigieneFactory(
            codigo=1,
            nombre_apellidos="Yisel de los Ángeles",
            laboratorio="Holguín",
            processed=True,
        )

        response = client.post(
            "/api/v1/placa/",
            {
                "nombre_apellidos": "Yisel de los Ángeles",
                "laboratorio": "Holguín",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_entry_processed_supervisor(self):
        group = factories.SupervisorGroupFactory()
        user = factories.UserFactory(groups=[group])
        client.force_authenticate(user=user)

        models.TestResult.objects.create(nombre="positivo")
        models.TestResult.objects.create(nombre="pendiente")

        factories.DataHigieneFactory(
            codigo=1,
            nombre_apellidos="Yisel de los Ángeles",
            laboratorio="Holguín",
            processed=True,
        )

        response = client.post(
            "/api/v1/placa/",
            {
                "nombre_apellidos": "Yisel de los Ángeles",
                "laboratorio": "Holguín",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_result_none_capturador(self):
        group = factories.CapturadorGroupFactory()
        user = factories.UserFactory(groups=[group])
        client.force_authenticate(user=user)

        factories.DataHigieneFactory(
            codigo=1,
            nombre_apellidos="Yisel de los Ángeles",
            laboratorio="Holguín",
            municipio="Bayamo",
        )

        response = client.post(
            "/api/v1/placa/",
            {
                "nombre_apellidos": "Yisel de los Ángeles",
                "laboratorio": "Holguín",
                "resultado": "positivo",
                "municipio": "Bayamo",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)

        data = models.DataEpidemiologiaModel.objects.first()
        higiene = models.DataHigieneModel.objects.first()

        self.assertFalse(higiene.processed)
        self.assertEqual(data.resultado, "PENDIENTE")
        self.assertIsNone(data.fecha_resultado)

    def test_result_none_supervisor(self):
        group = factories.SupervisorGroupFactory()
        user = factories.UserFactory(groups=[group])
        client.force_authenticate(user=user)

        factories.DataHigieneFactory(
            codigo=1,
            nombre_apellidos="Yisel de los Ángeles",
            laboratorio="Holguín",
            municipio="Bayamo",
        )

        response = client.post(
            "/api/v1/placa/",
            {
                "nombre_apellidos": "Yisel de los Ángeles",
                "laboratorio": "Holguín",
                "resultado": "positivo",
                "municipio": "Bayamo",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)

        data = models.DataEpidemiologiaModel.objects.first()
        higiene = models.DataHigieneModel.objects.first()

        self.assertFalse(higiene.processed)
        self.assertEqual(data.resultado, "PENDIENTE")
        self.assertIsNone(data.fecha_resultado)

    def test_update_result_capturador(self):
        group = factories.CapturadorGroupFactory()
        user = factories.UserFactory(groups=[group])
        client.force_authenticate(user=user)

        models.TestResult.objects.create(nombre="positivo")
        models.TestResult.objects.create(nombre="pendiente")

        factories.DataHigieneFactory(
            codigo=1,
            nombre_apellidos="Yisel de los Ángeles",
            laboratorio="Holguín",
            ci_pasaporte="850524321",
            edad=45,
        )

        response = client.post(
            "/api/v1/placa/",
            {
                "nombre_apellidos": "Yisel de los Ángeles",
                "laboratorio": "Holguín",
                "resultado": "POSITIVO",
                "fecha_resultado": "1985-03-02",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        epidemiologia = models.DataEpidemiologiaModel.objects.first()
        higiene = models.DataHigieneModel.objects.first()

        self.assertTrue(higiene.processed)
        self.assertEqual(epidemiologia.resultado, "POSITIVO")
        self.assertEqual(epidemiologia.fecha_resultado, date(1985, 3, 2))

    def test_update_result_supervisor(self):
        group = factories.SupervisorGroupFactory()
        user = factories.UserFactory(groups=[group])
        client.force_authenticate(user=user)

        models.TestResult.objects.create(nombre="positivo")
        models.TestResult.objects.create(nombre="pendiente")

        factories.DataHigieneFactory(
            codigo=1,
            nombre_apellidos="Yisel de los Ángeles",
            laboratorio="Holguín",
            ci_pasaporte="850524321",
            edad=45,
        )

        response = client.post(
            "/api/v1/placa/",
            {
                "nombre_apellidos": "Yisel de los Ángeles",
                "laboratorio": "Holguín",
                "resultado": "POSITIVO",
                "fecha_resultado": "1985-03-02",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        epidemiologia = models.DataEpidemiologiaModel.objects.first()
        higiene = models.DataHigieneModel.objects.first()

        self.assertTrue(higiene.processed)
        self.assertEqual(epidemiologia.resultado, "POSITIVO")
        self.assertEqual(epidemiologia.fecha_resultado, date(1985, 3, 2))

    def test_resultado_desconocido_capturador(self):
        group = factories.CapturadorGroupFactory()
        user = factories.UserFactory(groups=[group])
        client.force_authenticate(user=user)

        factories.DataHigieneFactory(
            codigo=1,
            nombre_apellidos="Yisel de los Ángeles",
            laboratorio="Holguín",
            municipio="Bayamo",
            ci_pasaporte="850524321",
            edad=45,
        )

        response = client.post(
            "/api/v1/placa/",
            {
                "nombre_apellidos": "Yisel de los Ángeles",
                "laboratorio": "Holguín",
                "municipio": "Bayamo",
                "ci": "850524321",
                "edad": 45,
                "resultado": "pendente",
                "fecha_resultado": "2021-05-30",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        epidemiologia = models.DataEpidemiologiaModel.objects.first()
        higiene = models.DataHigieneModel.objects.first()

        self.assertTrue(higiene.processed)
        self.assertEqual(epidemiologia.resultado, "PENDENTE")
        self.assertEqual(epidemiologia.fecha_resultado, date(2021, 5, 30))

    def test_resultado_desconocido_supervisor(self):
        group = factories.SupervisorGroupFactory()
        user = factories.UserFactory(groups=[group])
        client.force_authenticate(user=user)

        factories.DataHigieneFactory(
            codigo=1,
            nombre_apellidos="Yisel de los Ángeles",
            laboratorio="Holguín",
            municipio="Bayamo",
            ci_pasaporte="850524321",
            edad=45,
        )

        response = client.post(
            "/api/v1/placa/",
            {
                "nombre_apellidos": "Yisel de los Ángeles",
                "laboratorio": "Holguín",
                "municipio": "Bayamo",
                "ci": "850524321",
                "edad": 45,
                "resultado": "pendente",
                "fecha_resultado": "2021-05-30",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        epidemiologia = models.DataEpidemiologiaModel.objects.first()
        higiene = models.DataHigieneModel.objects.first()

        self.assertTrue(higiene.processed)
        self.assertEqual(epidemiologia.resultado, "PENDENTE")
        self.assertEqual(epidemiologia.fecha_resultado, date(2021, 5, 30))

    def test_resultado_pendiente_capturador(self):
        group = factories.CapturadorGroupFactory()
        user = factories.UserFactory(groups=[group])
        client.force_authenticate(user=user)

        models.TestResult.objects.create(nombre="positivo")
        models.TestResult.objects.create(nombre="pendiente")
        factories.DataHigieneFactory(
            codigo=1,
            nombre_apellidos="Yisel de los Ángeles",
            laboratorio="Holguín",
            municipio="Bayamo",
            ci_pasaporte="850524321",
            edad=45,
        )

        response = client.post(
            "/api/v1/placa/",
            {
                "nombre_apellidos": "Yisel de los Ángeles",
                "laboratorio": "Holguín",
                "municipio": "Bayamo",
                "ci": "850524321",
                "edad": 45,
                "resultado": "pendente",
                "fecha_resultado": "2021-05-30",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        epidemiologia = models.DataEpidemiologiaModel.objects.first()
        higiene = models.DataHigieneModel.objects.first()

        self.assertTrue(higiene.processed)
        self.assertEqual(epidemiologia.resultado, "PENDIENTE")
        self.assertEqual(epidemiologia.fecha_resultado, date(2021, 5, 30))

    def test_resultado_pendiente_supervisor(self):
        group = factories.SupervisorGroupFactory()
        user = factories.UserFactory(groups=[group])
        client.force_authenticate(user=user)

        models.TestResult.objects.create(nombre="positivo")
        models.TestResult.objects.create(nombre="pendiente")
        factories.DataHigieneFactory(
            codigo=1,
            nombre_apellidos="Yisel de los Ángeles",
            laboratorio="Holguín",
            municipio="Bayamo",
            ci_pasaporte="850524321",
            edad=45,
        )

        response = client.post(
            "/api/v1/placa/",
            {
                "nombre_apellidos": "Yisel de los Ángeles",
                "laboratorio": "Holguín",
                "municipio": "Bayamo",
                "ci": "850524321",
                "edad": 45,
                "resultado": "pendente",
                "fecha_resultado": "2021-05-30",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        epidemiologia = models.DataEpidemiologiaModel.objects.first()
        higiene = models.DataHigieneModel.objects.first()

        self.assertTrue(higiene.processed)
        self.assertEqual(epidemiologia.resultado, "PENDIENTE")
        self.assertEqual(epidemiologia.fecha_resultado, date(2021, 5, 30))

    def test_many_register_without_process_capturador(self):
        group = factories.CapturadorGroupFactory()
        user = factories.UserFactory(groups=[group])
        client.force_authenticate(user=user)

        models.TestResult.objects.create(nombre="positivo")
        models.TestResult.objects.create(nombre="pendiente")
        factories.DataHigieneFactory(
            codigo=1,
            nombre_apellidos="Yisel de los Ángeles",
            laboratorio="Holguín",
            municipio="Bayamo",
            ci_pasaporte="850524321",
            edad=45,
        )
        factories.DataHigieneFactory(
            codigo=2,
            nombre_apellidos="Yisel de los Ángeles",
            laboratorio="Holguín",
            municipio="Bayamo",
            ci_pasaporte="850524321",
            edad=45,
        )

        epi1 = models.DataEpidemiologiaModel.objects.get(no_muestra=1)
        epi1.fecha_resultado = date(2020, 5, 6)
        epi1.save()

        epi2 = models.DataEpidemiologiaModel.objects.get(no_muestra=2)
        epi2.fecha_resultado = date(2020, 5, 6)
        epi2.save()

        response = client.post(
            "/api/v1/placa/",
            {
                "nombre_apellidos": "Yisel de los Ángeles",
                "laboratorio": "Holguín",
                "resultado": "POSITIVO",
                "fecha_resultado": "2021-5-30",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        epidemiologia_first = models.DataEpidemiologiaModel.objects.first()
        epidemiologia = models.DataEpidemiologiaModel.objects.last()
        higiene_first = models.DataHigieneModel.objects.first()
        higiene = models.DataHigieneModel.objects.last()

        self.assertFalse(higiene_first.processed)
        self.assertTrue(higiene.processed)
        self.assertEqual(epidemiologia_first.resultado, "PENDIENTE")
        self.assertEqual(epidemiologia.resultado, "POSITIVO")
        self.assertEqual(epidemiologia_first.fecha_resultado, date(2020, 5, 6))
        self.assertEqual(epidemiologia.fecha_resultado, date(2021, 5, 30))

    def test_many_register_without_process_supervisor(self):
        group = factories.SupervisorGroupFactory()
        user = factories.UserFactory(groups=[group])
        client.force_authenticate(user=user)

        models.TestResult.objects.create(nombre="positivo")
        models.TestResult.objects.create(nombre="pendiente")
        factories.DataHigieneFactory(
            codigo=1,
            nombre_apellidos="Yisel de los Ángeles",
            laboratorio="Holguín",
            municipio="Bayamo",
            ci_pasaporte="850524321",
            edad=45,
        )
        factories.DataHigieneFactory(
            codigo=2,
            nombre_apellidos="Yisel de los Ángeles",
            laboratorio="Holguín",
            municipio="Bayamo",
            ci_pasaporte="850524321",
            edad=45,
        )

        epi1 = models.DataEpidemiologiaModel.objects.get(no_muestra=1)
        epi1.fecha_resultado = date(2020, 5, 6)
        epi1.save()

        epi2 = models.DataEpidemiologiaModel.objects.get(no_muestra=2)
        epi2.fecha_resultado = date(2020, 5, 6)
        epi2.save()

        response = client.post(
            "/api/v1/placa/",
            {
                "nombre_apellidos": "Yisel de los Ángeles",
                "laboratorio": "Holguín",
                "resultado": "POSITIVO",
                "fecha_resultado": "2021-5-30",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        epidemiologia_first = models.DataEpidemiologiaModel.objects.first()
        epidemiologia = models.DataEpidemiologiaModel.objects.last()
        higiene_first = models.DataHigieneModel.objects.first()
        higiene = models.DataHigieneModel.objects.last()

        self.assertFalse(higiene_first.processed)
        self.assertTrue(higiene.processed)
        self.assertEqual(epidemiologia_first.resultado, "PENDIENTE")
        self.assertEqual(epidemiologia.resultado, "POSITIVO")
        self.assertEqual(epidemiologia_first.fecha_resultado, date(2020, 5, 6))
        self.assertEqual(epidemiologia.fecha_resultado, date(2021, 5, 30))

    def test_sample_already_diagnosed_capturador(self):
        group = factories.CapturadorGroupFactory()
        user = factories.UserFactory(groups=[group])
        client.force_authenticate(user=user)

        models.TestResult.objects.create(nombre="Positivo")
        models.TestResult.objects.create(nombre="Negativo")
        factories.DataHigieneFactory(
            codigo=1,
            nombre_apellidos="Yisel de los Ángeles",
            laboratorio="Holguín",
            municipio="Bayamo",
            ci_pasaporte="850524321",
            edad=45,
        )
        sample = models.DataEpidemiologiaModel.objects.filter(no_muestra=1)
        sample.update(resultado="Positivo")

        with self.settings(POSITIVE_TEST="Positivo"):
            response = client.post(
                "/api/v1/placa/",
                {
                    "nombre_apellidos": "Yisel de los Ángeles",
                    "laboratorio": "Holguín",
                    "resultado": "Negativo",
                    "fecha_resultado": "2021-5-30",
                    "hora": "12:40",
                },
                format="json",
            )

        self.assertEqual(response.status_code, 400)
        error = response.data["resultado"][0]
        self.assertEqual(error.code, "diagnosed")

    def test_sample_already_diagnosed_supervisor(self):
        group = factories.SupervisorGroupFactory()
        user = factories.UserFactory(groups=[group])
        client.force_authenticate(user=user)

        models.TestResult.objects.create(nombre="Positivo")
        models.TestResult.objects.create(nombre="Negativo")
        factories.DataHigieneFactory(
            codigo=1,
            nombre_apellidos="Yisel de los Ángeles",
            laboratorio="Holguín",
            municipio="Bayamo",
            ci_pasaporte="850524321",
            edad=45,
        )
        sample = models.DataEpidemiologiaModel.objects.filter(no_muestra=1)
        sample.update(resultado="Positivo")

        with self.settings(POSITIVE_TEST="Positivo"):
            response = client.post(
                "/api/v1/placa/",
                {
                    "nombre_apellidos": "Yisel de los Ángeles",
                    "laboratorio": "Holguín",
                    "resultado": "Negativo",
                    "fecha_resultado": "2021-5-30",
                    "hora": "12:40",
                },
                format="json",
            )

        self.assertEqual(response.status_code, 400)
        error = response.data["resultado"][0]
        self.assertEqual(error.code, "diagnosed")


class MediaRetrieveTest(TestCase):
    def test_anonymous_user(self):
        with self.settings(LOGIN_URL="/login/"):
            url = "/media/file.xlsx"
            response = client.get(url)
            expected = "/login/?next=/media/file.xlsx"

            self.assertRedirects(
                response, expected, fetch_redirect_response=False
            )

    def test_path_not_found(self):
        user = factories.UserFactory()
        client.force_login(user)
        response = client.get("/media/file.xlsx")

        self.assertEqual(response.status_code, 200)
