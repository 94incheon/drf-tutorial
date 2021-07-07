from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination


class WatchListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'size'
    max_page_size = 10
    last_page_strings = ('last', )


class WatchListLOPagination(LimitOffsetPagination):
    default_limit = 5
    limit_query_param = 'limit'
    offset_query_param = 'start'
    max_limit = 5


class WatchListCursorPagination(CursorPagination):
    page_size = 5
    cursor_query_param = 'record'
    ordering = '-number_rating'
