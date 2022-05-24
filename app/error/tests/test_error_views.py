from django.test import TestCase, override_settings
from rest_framework.test import APIClient


# ROOT_URLCONF must specify the module that contains handler403 = ...
@override_settings(ROOT_URLCONF="error.urls", DEBUG=False)
class CustomErrorHandlerTests(TestCase):

    client = APIClient()

    def test_handler_400(self):
        response = self.client.get("/400/")
        self.assertContains(response, "400", status_code=400)

    def test_handler_403(self):
        response = self.client.get("/403/")
        self.assertContains(response, "403", status_code=403)

    def test_handler_404(self):
        response = self.client.get("/404/")
        self.assertContains(response, "404", status_code=404)

    def test_handler_500(self):
        response = self.client.get("/500/")
        self.assertContains(response, "500", status_code=500)
