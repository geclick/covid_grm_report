from django.urls import path
from django.shortcuts import render


def page_not_found(request):
    # Dict to pass to template, data could come from DB query
    values_for_template = {
        "code": 404,
        "message": "NO FUE ENCONTRADO",
        "enc": "EL RECURSO",
    }
    return render(request, "error/404.html", values_for_template, status=404)


def server_error(request):
    # Dict to pass to template, data could come from DB query
    values_for_template = {}
    return render(request, "error/50x.html", values_for_template, status=500)


def bad_request(request):
    # Dict to pass to template, data could come from DB query
    values_for_template = {
        "code": 400,
        "message": "Petición incorrecta",
        "enc": "",
    }
    return render(request, "error/404.html", values_for_template, status=400)


def permission_denied(request):
    # Dict to pass to template, data could come from DB query
    values_for_template = {}
    return render(request, "error/403.html", values_for_template, status=403)


urlpatterns = [
    path("403/", permission_denied),
    path("404/", page_not_found),
    path("400/", bad_request),
    path("500/", server_error),
]
