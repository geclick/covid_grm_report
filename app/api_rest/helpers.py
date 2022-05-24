from rest_framework import serializers

from . import serializer as api_serializers


def diagnose(sample, **data):
    """
    Update PCR sample result

    Args:
        sample (DataEpidemiologiaModel): sample
        result (str): sample result
        result_date (date): date of result

    Raises:
        ValidationError: Error in validation of data
    """

    try:
        serializer = api_serializers.DataLaboratorySerializer(
            sample, data=data
        )  # serializador para insertar resultados de muestras
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return serializer
    except serializers.ValidationError as e:
        error = e.detail.get("resultado")
        if error and error[0].code == "diagnosed":
            new_resultado = data.get("resultado")
            new_fecha_resultado = data.get("fecha_resultado")

            data = {
                "sample": sample.pk,
                "result": sample.resultado,
                "result_date": sample.fecha_resultado,
            }
            if new_resultado:
                data.update({"new_result": new_resultado})
            if new_fecha_resultado:
                data.update({"new_result_date": new_fecha_resultado})

            serializer = api_serializers.ResultRegisterSerializer(data=data)
            if serializer.is_valid():
                serializer.save()

        raise e
