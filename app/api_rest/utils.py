from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.utils.html import format_html
from fuzzywuzzy import process

from api_rest import models


def lab_directory_path(instance, filename):
    """
    Determinate directory path for lab results, return the path

    Arguments
    instance - Activity report instance
    filename - name of activity report file
    """
    root = settings.LAB_DIR
    suffix = Path(instance.archivo.path).suffix
    id = str(datetime.now().timestamp()).replace(".", "_")
    lab = instance.laboratorio.nombre.upper()
    lab_procesado = instance.lab_procesado.nombre.upper()
    strdate = instance.fecha.strftime("%Y%m%d")
    hm = instance.fecha.strftime("%H-%M")

    return f"{root}{lab}-{strdate}-{lab_procesado}_{hm}_{id}{suffix}"


def higiene_directory_path(instance, filename):
    """
    Determinate directory path for lab results, return the path

    Arguments
    instance - Activity report instance
    filename - name of activity report file
    """
    root = settings.HIGIENE_DIR
    suffix = Path(instance.archivo.path).suffix
    laboratory = instance.laboratorio.nombre.upper()
    strdate = instance.fecha.strftime("%d%m%Y")
    id = str(datetime.now().timestamp()).replace(".", "_")

    return f"{root}{laboratory}-{strdate}_{id}{suffix}"


def epidemiologia_directory_path(instance, filename):
    """
    Determinate directory path for lab results, return the path

    Arguments
    instance - Activity report instance
    filename - name of activity report file
    """
    root = settings.EPIDEMIOLOGIA_DIR
    suffix = Path(instance.archivo.path).suffix
    strdate = instance.fecha.strftime("%d%m%Y")
    id = str(datetime.now().timestamp()).replace(".", "_")

    return f"{root}bd-{strdate}_{id}{suffix}"


def uploaded_file_current_path(file, processed_destination_path):
    """
    Determinate directory path for lab results, return the path

    Arguments
    file - the uploaded file reference
    processed_destination_path - path for processed files according its model
    """
    path = Path(file.path)

    if path.exists():

        # file.name contains shared/name_of_folder
        # Ex: shared/lab/file_name.extension
        # so I use file.name to get the relative path inside media folder

        html = '<a href="{}" target="_blank" >{}</a>'.format(
            settings.PROTECTED_MEDIA_URL + file.name, path.name
        )
        return format_html(html)
    else:
        if len(path.parts):
            # only name of file without any path, just name and extension
            filename = path.parts[-1]

            processed_path = (
                settings.PROTECTED_MEDIA_ROOT
                + "/"  # noqa: W503
                + processed_destination_path  # noqa: W503
                + filename  # noqa: W503
            )

            path = Path(processed_path)

            if path.exists():
                html = '<a href="{}" target="_blank">{}</a>'.format(
                    settings.PROTECTED_MEDIA_URL
                    + processed_destination_path
                    + filename,
                    path.name,
                )
                return format_html(html)

    return format_html('<a href="">No se encontró al archivo</a>')


class LabViesetConfig:
    fixed_filters = [
        ("laboratorio", "__iexact"),
        ("nombre_apellidos", "__iexact"),
    ]

    optionals_filter = []

    data_keys = ["resultado", "fecha_resultado", "ct", "hora"]

    map = {
        "laboratorio": "laboratorio",
        "nombre_apellidos": "nombre_apellidos",
        "ci": "ci_pasaporte",
        "sexo": "sexo",
        "edad": "edad",
        "provincia": "provincia",
        "municipio": "municipio",
    }

    def data(self, data):
        data = {k: v for k, v in data.items() if k in self.data_keys}

        # Standardize resultado
        resultado = data.get("resultado")
        if resultado:
            resultado = match_test_result(resultado)

        data.update({"resultado": resultado})

        return data

    def filters(self, data):
        filters = {
            f"{self.map[k[0]]}{k[1]}": data.get(k[0])
            for k in self.fixed_filters
        }
        optionals = self.bypass(
            data,
            self.optionals_filter,
            self.map,
        )
        filters.update(optionals)

        return filters

    def bypass(self, data, fields, map):
        return {
            f"{self.map[k[0]]}{k[1]}": data.get(k[0])
            for k in fields
            if k[0] in data
        }


def match_test_result(result):
    """
    Match result between posibles results

    Args:
        result (str): result to match
    Returns:
        result with highest similarity
    """
    posibles = models.TestResult.objects.values_list("nombre", flat=True)
    if posibles:
        match, _ = process.extractOne(result, list(posibles))
    else:
        match = result

    return match.upper()


def epidemiologia_data_map(instance):
    """
    Map between higiene and epidemiologia data

    Args:
        instance (dict) higiene instance
    Returns:
        epidemiologia data (dict)
    """

    return {
        "no_muestra": instance.codigo,
        "laboratorio": instance.laboratorio,
        "nombre_apellido": instance.nombre_apellidos,
        "ci_pasaporte": instance.ci_pasaporte,
        "edad": instance.edad,
        "sexo": instance.sexo,
        "direccion": instance.direccion,
        "municipio": instance.municipio,
        "fis": instance.f_inicio_sintomas,
        "ftm": instance.fecha_toma_muestra,
        "fecha_envio": instance.fecha_envio,
        "condicion": instance.condicion,
        "pais": instance.pais_procedencia,
        "muestra": instance.tipo_muestra,
        "aislamiento": instance.procedencia_entrega
        if instance.procedencia_entrega
        else instance.area_salud,
    }


def uploaded_file_state(
    file, processed_destination_path, with_error, error_link
):
    """
    Determinate state of current uploaded file(pending, processed or unknown)

    Arguments
    file - the uploaded file reference
    processed_destination_path - path for processed files according its model
    """
    path = Path(file.path)

    html = '<a href="{}" style="color:#{}; "target="_blank">{}{}</a>'
    error_symbol = ""

    if path.exists():

        # file.name contains shared/name_of_folder
        # Ex: shared/lab/file_name.extension
        # so I use file.name to get the relative path inside media folder

        return format_html(
            html.format(error_link, "2e00ff", "PENDIENTE", error_symbol)
        )

    else:

        if len(path.parts):
            # only name of file without any path, just name and extension
            filename = path.parts[-1]

            processed_path = (
                settings.PROTECTED_MEDIA_ROOT
                + "/"  # noqa: W503
                + processed_destination_path  # noqa: W503
                + filename  # noqa: W503
            )
            path = Path(processed_path)

            color = "4ec918"
            if with_error:
                color = "FF0000"
                error_symbol = "(CON ERRORES)"

            if path.exists():
                return format_html(
                    html.format(error_link, color, "PROCESADO", error_symbol)
                )

    return format_html(
        html.format(error_link, "000000", "DESCONOCIDO", error_symbol)
    )


def error_filename_path(
    filename, destination_path, processed_destination_path
):
    """
    Determinate directory path for lab results, return the path

    Arguments
    filename - the filename
    processed_destination_path - path for processed files according its model
    """
    path = Path(destination_path + filename)

    if path.exists():

        # file.name contains shared/name_of_folder
        # Ex: shared/lab/file_name.extension
        # so I use file.name to get the relative path inside media folder

        return settings.PROTECTED_MEDIA_URL + filename
    else:
        processed_path = (
            settings.PROTECTED_MEDIA_ROOT
            + "/"  # noqa: W503
            + processed_destination_path  # noqa: W503
            + filename  # noqa: W503
        )

        path = Path(processed_path)

        if path.exists():
            return (
                settings.PROTECTED_MEDIA_URL
                + processed_destination_path  # noqa: W503
                + filename  # noqa: W503
            )

    return "#DESCONOCIDO"


def overrides(interface_class):
    def overrider(method):
        assert method.__name__ in dir(interface_class)
        return method

    return overrider
