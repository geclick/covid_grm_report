from django.test import TestCase
from rest_framework.test import APIClient

from api_rest.tests.factories import (
    UserFactory,
    InvitadoGroupFactory,
    CapturadorGroupFactory,
    SupervisorGroupFactory,
)

from error import models

from . import factories


client = APIClient()


class HigieneErrorListTest(TestCase):
    def test_no_permission(self):
        user = UserFactory()
        client.force_authenticate(user=user)

        response = client.get("/api/v1/higiene-errores/", format="json")

        self.assertEqual(response.status_code, 403)

    def test_succes_invitado(self):
        group = InvitadoGroupFactory()
        user = UserFactory(groups=[group])
        client.force_authenticate(user=user)

        factories.DataHigieneErrorFactory()

        response = client.get("/api/v1/higiene-errores/", format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.DataHigieneError.objects.count(), 1)

    def test_succes_capturador(self):
        group = CapturadorGroupFactory()
        user = UserFactory(groups=[group])
        client.force_authenticate(user=user)

        factories.DataHigieneErrorFactory()

        response = client.get("/api/v1/higiene-errores/", format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.DataHigieneError.objects.count(), 1)

    def test_succes_supervisor(self):
        group = SupervisorGroupFactory()
        user = UserFactory(groups=[group])
        client.force_authenticate(user=user)

        factories.DataHigieneErrorFactory()

        response = client.get("/api/v1/higiene-errores/", format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.DataHigieneError.objects.count(), 1)


class HigieneErrorCreateTest(TestCase):
    def test_create_success_root(self):
        user = UserFactory(is_superuser=True)
        client.force_authenticate(user=user)

        response = client.post(
            "/api/v1/higiene-errores/",
            {"msg": "error", "nombre_archivo": "reporte.xls"},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(models.DataHigieneError.objects.count(), 1)

    def test_create_success_capturador(self):
        group = CapturadorGroupFactory()
        user = UserFactory(groups=[group])
        client.force_authenticate(user=user)

        response = client.post(
            "/api/v1/higiene-errores/",
            {"msg": "error", "nombre_archivo": "reporte.xls"},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(models.DataHigieneError.objects.count(), 1)

    def test_create_success_supervisor(self):
        group = SupervisorGroupFactory()
        user = UserFactory(groups=[group])
        client.force_authenticate(user=user)

        response = client.post(
            "/api/v1/higiene-errores/",
            {"msg": "error", "nombre_archivo": "reporte.xls"},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(models.DataHigieneError.objects.count(), 1)


class DataEpidemiologiaErrorListTest(TestCase):
    def test_no_permission(self):
        user = UserFactory()
        client.force_authenticate(user=user)

        response = client.get("/api/v1/epidemiologia-errores/", format="json")

        self.assertEqual(response.status_code, 403)

    def test_succes_invitado(self):
        group = InvitadoGroupFactory()
        user = UserFactory(groups=[group])
        client.force_authenticate(user=user)

        factories.DataEpidemiologiaErrorFactory()

        response = client.get("/api/v1/epidemiologia-errores/", format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.DataEpidemiologiaError.objects.count(), 1)

    def test_succes_capturador(self):
        group = CapturadorGroupFactory()
        user = UserFactory(groups=[group])
        client.force_authenticate(user=user)

        factories.DataEpidemiologiaErrorFactory()

        response = client.get("/api/v1/epidemiologia-errores/", format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.DataEpidemiologiaError.objects.count(), 1)

    def test_succes_supervisor(self):
        group = SupervisorGroupFactory()
        user = UserFactory(groups=[group])
        client.force_authenticate(user=user)

        factories.DataEpidemiologiaErrorFactory()

        response = client.get("/api/v1/epidemiologia-errores/", format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.DataEpidemiologiaError.objects.count(), 1)


class DataEpidemiologiaErrorCreateTest(TestCase):
    def test_create_success_root(self):
        user = UserFactory(is_superuser=True)
        client.force_authenticate(user=user)

        response = client.post(
            "/api/v1/epidemiologia-errores/",
            {"msg": "error", "nombre_archivo": "reporte.xls"},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(models.DataEpidemiologiaError.objects.count(), 1)

    def test_create_success_capturador(self):
        group = CapturadorGroupFactory()
        user = UserFactory(groups=[group])
        client.force_authenticate(user=user)

        response = client.post(
            "/api/v1/epidemiologia-errores/",
            {"msg": "error", "nombre_archivo": "reporte.xls"},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(models.DataEpidemiologiaError.objects.count(), 1)

    def test_create_success_supervisor(self):
        group = SupervisorGroupFactory()
        user = UserFactory(groups=[group])
        client.force_authenticate(user=user)

        response = client.post(
            "/api/v1/epidemiologia-errores/",
            {"msg": "error", "nombre_archivo": "reporte.xls"},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(models.DataEpidemiologiaError.objects.count(), 1)


class PlacaErrorListTest(TestCase):
    def test_no_permission(self):
        user = UserFactory()
        client.force_authenticate(user=user)

        response = client.get("/api/v1/placa-errores/", format="json")

        self.assertEqual(response.status_code, 403)

    def test_succes_invitado(self):
        group = InvitadoGroupFactory()
        user = UserFactory(groups=[group])
        client.force_authenticate(user=user)

        factories.PlacaErrorFactory()

        response = client.get("/api/v1/placa-errores/", format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.PlacaErrorModel.objects.count(), 1)

    def test_succes_capturador(self):
        group = CapturadorGroupFactory()
        user = UserFactory(groups=[group])
        client.force_authenticate(user=user)

        factories.PlacaErrorFactory()

        response = client.get("/api/v1/placa-errores/", format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.PlacaErrorModel.objects.count(), 1)

    def test_succes_supervisor(self):
        group = SupervisorGroupFactory()
        user = UserFactory(groups=[group])
        client.force_authenticate(user=user)

        factories.PlacaErrorFactory()

        response = client.get("/api/v1/placa-errores/", format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.PlacaErrorModel.objects.count(), 1)


class PlacaErrorCreateTest(TestCase):
    def test_create_success_root(self):
        user = UserFactory(is_superuser=True)
        client.force_authenticate(user=user)

        response = client.post(
            "/api/v1/placa-errores/",
            {"msg": "error", "nombre_archivo": "reporte.xls"},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(models.PlacaErrorModel.objects.count(), 1)

    def test_create_success_capturador(self):
        group = CapturadorGroupFactory()
        user = UserFactory(groups=[group])
        client.force_authenticate(user=user)

        response = client.post(
            "/api/v1/placa-errores/",
            {"msg": "error", "nombre_archivo": "reporte.xls"},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(models.PlacaErrorModel.objects.count(), 1)

    def test_create_success_supervisor(self):
        group = SupervisorGroupFactory()
        user = UserFactory(groups=[group])
        client.force_authenticate(user=user)

        response = client.post(
            "/api/v1/placa-errores/",
            {"msg": "error", "nombre_archivo": "reporte.xls"},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(models.PlacaErrorModel.objects.count(), 1)
