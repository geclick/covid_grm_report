from django.conf.urls import include
from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from .views import (
    DataEpidemiologiaViewset,
    DataHigieneViewset,
    LabViewSet,
    EpidemiologiaXLSView,
    MunicipioViewset,
)
from error.views import (
    DataHigieneErrorViewset,
    DataEpidemiologiaErrorViewset,
)
from error.views import PlacaErrorViewset

app_name = "api_rest"


router = routers.DefaultRouter()
router.register("higiene", DataHigieneViewset, "higiene")
router.register("higiene-errores", DataHigieneErrorViewset)
router.register("epidemiologia", DataEpidemiologiaViewset, "epidemiologia")
router.register("epidemiologia-errores", DataEpidemiologiaErrorViewset)
router.register("placa", LabViewSet, "laboratorio")
router.register("placa-errores", PlacaErrorViewset)
router.register("municipio", MunicipioViewset)


schema_view = get_schema_view(
    openapi.Info(
        title="GRM COVID-19 Data Portal REST API",
        default_version="v1",
        description="Api Rest del Proyecto GRM COVID-19 Data Portal",
        contact=openapi.Contact(email="eperezm@udg.co.cu"),
        license=openapi.License(name="GPL"),
    ),
    # url='https://pcr.grm.sld.cu/api/v1/',
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(
        r"^schema(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("", include(router.urls)),
    path(
        "docs/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    # JWT auth
    path(r"session/obtain_token/", obtain_jwt_token),
    path(r"session/refresh_token/", refresh_jwt_token),
    path(
        r"epidemiologia/xlsx",
        EpidemiologiaXLSView.as_view({"get": "list"}),
        name="xls_epidemiologia",
    ),
]
