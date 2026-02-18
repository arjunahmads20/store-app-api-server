from rest_framework import viewsets
from .models import Store
from .serializers import StoreSerializer

class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['name', 'datetime_added']
    ordering = ['-datetime_added']
