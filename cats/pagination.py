from rest_framework.pagination import PageNumberPagination


class CatsPagination(PageNumberPagination):
    page_size = 20

    # paginate_queryset(self, queryset, request, view=None)
    # get_paginated_response(self, data)
