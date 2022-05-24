from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ApiRestConfig(AppConfig):
    name = "api_rest"
    verbose_name = _("Covid GRM Report")
    verbose_name_plural = _("Covid GRM Reports")
