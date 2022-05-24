# filtering.py
from django_filters.rest_framework import DjangoFilterBackend


def sort_queryset(queryset, field):
    if field:
        return queryset.order_by(field)

    return queryset


class ReactAdminFilterBackend(DjangoFilterBackend):
    def get_filterset_kwargs(self, request, queryset, view):
        for key, value in request.query_params.items():
            if key == "ordering" and value:
                queryset = sort_queryset(queryset, value)

        return {
            "data": request.query_params,
            "queryset": queryset,
            "request": request,
        }
