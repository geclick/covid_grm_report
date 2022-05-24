from django.contrib.auth.models import Permission
from rest_framework.permissions import DjangoModelPermissions, BasePermission


class AuthorizedAccessPermissions(DjangoModelPermissions):
    def __init__(self):
        self.perms_map["GET"] = ["%(app_label)s.view_%(model_name)s"]


class AddPlacaPermissions(BasePermission):
    """
    Allows access only to users with placa add permission.

    Created because LabViewSet doesn't define a queryset attribute or overrides
    get_queryset(), so the DjangoModelPermissions cannot be used
    """

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated
            and request.user.has_perms(["api_rest.add_dataepidemiologiamodel"])
        )


INVITADO_MODEL_PERMISSIONS = [
    "view_datahigienemodel",
    "view_dataepidemiologiamodel",
    "view_epidemiologiauploadmodel",
    "view_higieneuploadmodel",
    "view_laboratorio",
    "view_resultmodel",
    "view_resultregister",
    "view_testresult",
    "view_advancedfilter",
    "view_dataepidemiologiaerror",
    "view_datahigieneerror",
    "view_placaerrormodel",
]

CENTRO_MODEL_PERMISSIONS = ["view_dataepidemiologiamodel"]

CAPTURADOR_MODEL_PERMISSIONS = [
    "add_advancedfilter",
    "change_advancedfilter",
    "delete_advancedfilter",
    "view_advancedfilter",
    # DataEpidemiologiaModel
    "add_dataepidemiologiamodel",
    "change_dataepidemiologiamodel",
    "delete_dataepidemiologiamodel",
    "view_dataepidemiologiamodel",
    # DataHigieneModel
    "add_datahigienemodel",
    # HigieneUploadModel
    "add_higieneuploadmodel",
    "change_higieneuploadmodel",
    "delete_higieneuploadmodel",
    "view_higieneuploadmodel",
    # ResultModel
    "add_resultmodel",
    "change_resultmodel",
    "delete_resultmodel",
    "view_resultmodel",
    # ResultRegister
    "add_resultregister",
    "change_resultregister",
    "delete_resultregister",
    "view_resultregister",
    # DataEpidemiologiaError
    "add_dataepidemiologiaerror",
    "change_dataepidemiologiaerror",
    "delete_dataepidemiologiaerror",
    "view_dataepidemiologiaerror",
    # DataHigieneError
    "add_datahigieneerror",
    "change_datahigieneerror",
    "delete_datahigieneerror",
    "view_datahigieneerror",
    # PlacaErrorModel
    "add_placaerrormodel",
    "change_placaerrormodel",
    "delete_placaerrormodel",
    "view_placaerrormodel",
]

# se obvian permisos de logentry, group, permission, user, token, contentype
# y session
SUPERVISOR_MODEL_PERMISSIONS = [
    "add_advancedfilter",
    "change_advancedfilter",
    "delete_advancedfilter",
    "view_advancedfilter",
    # DataEpidemiologiaModel
    "add_dataepidemiologiamodel",
    "change_dataepidemiologiamodel",
    "delete_dataepidemiologiamodel",
    "view_dataepidemiologiamodel",
    # DataHigieneModel
    "add_datahigienemodel",
    "change_datahigienemodel",
    "delete_datahigienemodel",
    "view_datahigienemodel",
    # EpidemiologiaUploadModel
    "add_epidemiologiauploadmodel",
    "change_epidemiologiauploadmodel",
    "delete_epidemiologiauploadmodel",
    "view_epidemiologiauploadmodel",
    # HigieneUploadModel
    "add_higieneuploadmodel",
    "change_higieneuploadmodel",
    "delete_higieneuploadmodel",
    "view_higieneuploadmodel",
    # Laboratorio
    "view_laboratorio",
    # ResultModel
    "add_resultmodel",
    "change_resultmodel",
    "delete_resultmodel",
    "view_resultmodel",
    # ResultRegister
    "add_resultregister",
    "change_resultregister",
    "delete_resultregister",
    "view_resultregister",
    # TestResult
    "add_testresult",
    "change_testresult",
    "delete_testresult",
    "view_testresult",
    # DataEpidemiologiaError
    "add_dataepidemiologiaerror",
    "change_dataepidemiologiaerror",
    "delete_dataepidemiologiaerror",
    "view_dataepidemiologiaerror",
    # DataHigieneError
    "add_datahigieneerror",
    "change_datahigieneerror",
    "delete_datahigieneerror",
    "view_datahigieneerror",
    # PlacaErrorModel
    "add_placaerrormodel",
    "change_placaerrormodel",
    "delete_placaerrormodel",
    "view_placaerrormodel",
]

PERMISSIONS_PER_GROUP = {
    "INVITADO": INVITADO_MODEL_PERMISSIONS,
    "CAPTURADOR": CAPTURADOR_MODEL_PERMISSIONS,
    "CENTRO": CENTRO_MODEL_PERMISSIONS,
    "SUPERVISOR": SUPERVISOR_MODEL_PERMISSIONS,
}


def get_group_model_permissions(group_name):
    permissions = []
    list_str_permissions = PERMISSIONS_PER_GROUP[group_name]

    for str_perm in list_str_permissions:
        try:
            permissions.append(Permission.objects.get(codename=str_perm))
        except:  # noqa: E722
            pass

    return permissions
