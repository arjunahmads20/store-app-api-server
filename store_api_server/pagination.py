from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_query_param = 'page'
    page_size_query_param = 'page_size'  # Support ?page_size=40

    def get_page_number(self, request, paginator):
        page_param = request.query_params.get(self.page_query_param, '1')
        if ',' in page_param:
            parts = page_param.split(',')
            return parts[0]
        return page_param

    def get_page_size(self, request):
        # 1. Custom support: ?page=1,20
        page_param = request.query_params.get(self.page_query_param, '')
        if ',' in page_param:
            parts = page_param.split(',')
            if len(parts) > 1:
                return int(parts[1])
        
        # 2. Standard support: ?page_size=20 (via super)
        return super().get_page_size(request)

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
