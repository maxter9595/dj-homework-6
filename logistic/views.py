# from rest_framework import filters, status
# from rest_framework.pagination import LimitOffsetPagination
# from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from logistic.serializers import ProductSerializer, StockSerializer

from logistic.models import Product, Stock


class ProductViewSet(ModelViewSet):
    """
    ViewSet модели Product
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [
        SearchFilter,
    ]

    search_fields = [
        'title',
        'description'
    ]


class StockViewSet(ModelViewSet):
    """
    ViewSet модели Stock
    """
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    filter_backends = [
        SearchFilter,
    ]

    filterset_fields = [
        'products'
    ]

    search_fields = [
        'positions__product__title',
        'positions__product__description',
    ]
