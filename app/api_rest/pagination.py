# pagination.py
from collections import OrderedDict
from rest_framework.response import Response
from rest_framework.pagination import (
    PageNumberPagination,
    LimitOffsetPagination,
)


class ReactAdminPagination(PageNumberPagination):
    page_query_param = "page"
    page_size_query_param = "perPage"

    def get_paginated_response(self, data):
        count = self.page.paginator.count
        item_starting_index = self.page.start_index() - 1
        item_ending_index = self.page.end_index() - 1

        content_range = "items {0}-{1}/{2}".format(
            item_starting_index, item_ending_index, count
        )

        headers = {"Content-Range": content_range}

        return Response(
            OrderedDict(
                [
                    ("total", count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ]
            ),
            headers=headers,
        )


def _positive_int(integer_string, strict=False, cutoff=None):
    """
    Cast a string to a strictly positive integer.
    """
    ret = int(integer_string)
    if ret < 0 or (ret == 0 and strict):
        raise ValueError()
    if cutoff:
        return min(ret, cutoff)
    return ret


class StandardResultsSetPagination(LimitOffsetPagination):
    """This is to handle react-admins call to our API when paginating"""

    offset_query_param = "_start"

    def get_paginated_response(self, data):
        headers = {"X-Total-Count": self.count}
        response = Response(data, headers=headers)
        return response

    def get_limit(self, request):

        print("request query params..")
        print(request.query_params)
        try:
            end = request.query_params["_end"]
            start = request.query_params["_start"]
            limit = int(end) - int(start)
            return _positive_int(limit)

        except (KeyError, ValueError):
            pass

        return self.default_limit
