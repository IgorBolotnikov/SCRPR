from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


def get_pagination(self, paginator):
    prev_page = paginator.previous_page_number if paginator.has_previous else None
    next_page = paginator.next_page_number if paginator.has_next else None
    return {
        'page': paginator.number,
        'prev_page': prev_page,
        'next_page': next_page,
        'last_page': paginator.num_pages
    }

DEFAULT_PAGE = 1

class DetailedPagination(PageNumberPagination):
    page = DEFAULT_PAGE
    page_size = 10
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        page_size = int(self.request.GET.get('page_size', self.page_size))
        last_page = int(self.page.paginator.count / page_size)
        page = int(self.request.GET.get('page', DEFAULT_PAGE))
        next_page = page + 1 if page < last_page else None
        prev_page = page - 1 if page > 1 else None

        return Response({
            'pagination': {
                'page': page,
                'prev_page': prev_page,
                'next_page': next_page,
                'last_page': last_page,
                'page_size': page_size
            },
            'results': data
        })
