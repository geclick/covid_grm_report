from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DjangoServerAccessLogsConfig(AppConfig):
    name = "django_server_access_logs"
    verbose_name = _("Server Access Log")
    verbose_name_plural = _("Server Access Logs")
