from django.contrib import admin
from import_export import resources
from import_export.admin import ExportMixin
from . import models


class AccessLogsModelResource(resources.ModelResource):
    class Meta:
        model = models.AccessLogsModel
        exclude = "sys_id"
        export_order = (
            "session_key",
            "username",
            "path",
            "method",
            "data",
            "ip_address",
            "referrer",
            "timestamp",
        )
        verbose_name = "Log de acceso"
        verbose_name_plural = "Logs de Accesos"


class AccessLogsModelAdmin(ExportMixin, admin.ModelAdmin):

    resource_class = AccessLogsModelResource
    list_display = (
        "username",
        "session_key",
        "path",
        "method",
        "data",
        "ip_address",
        "referrer",
        "timestamp",
    )

    list_filter = ["method", "username", "ip_address", "timestamp"]

    search_fields = [
        "method",
        "ip_address",
        "method",
    ]
    ordering = ["-timestamp"]
    list_display_links = ("username",)


admin.site.register(models.AccessLogsModel, AccessLogsModelAdmin)
