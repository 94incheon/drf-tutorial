from rest_framework.pagination import PageNumberPagination


class WatchListPagination(PageNumberPagination):
    page_size = 3
    # page_query_param = 'p'  # ?p=2 (default: page)
    page_size_query_param = 'size'  # ?size=10 (number of data per page)
    max_page_size = 10  # ?size=12 로 요청해도 최대개수 10개까지만 반환한다. (위 옵션이 있어야만 작동한다.)
    last_page_strings = ('last', )  # ?page=last
