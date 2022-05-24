from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ErrorConfig(AppConfig):
    name = "error"
    verbose_name = _("Error")
    verbose_name_plural = _("Errores")
