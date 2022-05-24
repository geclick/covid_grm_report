from django.db import models


class AccessLogsModel(models.Model):
    sys_id = models.AutoField(primary_key=True, null=False, blank=True)
    username = models.CharField(
        max_length=100,
        null=False,
        blank=True,
        verbose_name="Nombre de Usuario",
    )
    session_key = models.CharField(max_length=1024, null=False, blank=True)
    path = models.CharField(
        max_length=1024, null=False, blank=True, verbose_name="Ruta"
    )
    method = models.CharField(
        max_length=8, null=False, blank=True, verbose_name="Método"
    )
    data = models.TextField(null=True, blank=True, verbose_name="Datos")
    ip_address = models.CharField(
        max_length=45, null=False, blank=True, verbose_name="Dirección IP"
    )
    referrer = models.CharField(
        max_length=512, null=True, blank=True, verbose_name="Referencia"
    )
    timestamp = models.DateTimeField(
        null=False, blank=True, verbose_name="Fecha y Hora"
    )

    class Meta:
        # app_label = "django_server_access_logs"
        db_table = "access_logs"
        verbose_name = "Log de Acceso"
        verbose_name_plural = "Logs de Accesos"
