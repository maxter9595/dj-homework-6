from rest_framework import filters, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from logistic.serializers import ProductSerializer, StockSerializer

from logistic.models import Product, Stock, StockProduct


class ProductViewSet(ModelViewSet):
    """
    ViewSet модели Product
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]

    filterset_fields = [
        'id',
    ]

    search_fields = [
        'title',
        'description'
    ]

    ordering_fields = [
        'id'
    ]

    pagination_class = LimitOffsetPagination

    def create(self, request, *args, **kwargs):
        """
        Отвечает за обработку запроса на создание
        новых экземпляров модели Product
        """
        data = request.data.get(
            'products',
            []
        )

        serializer = self.get_serializer(
            data=data,
            many=True
        )

        serializer.is_valid(
            raise_exception=True
        )

        self.perform_create(
            serializer
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class StockViewSet(ModelViewSet):
    """
    ViewSet модели Stock
    """
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    search_fields = [
        'positions__product__id',
        'positions__product__title',
        'positions__product__description',
    ]

    ordering_fields = [
        'id'
    ]

    pagination_class = LimitOffsetPagination

    def create(self, request, *args, **kwargs):
        """
        Используется для создания нового объекта модели Stock
        """
        data = request.data

        address = data.get(
            'address'
        )
        positions = data.get(
            'positions', []
        )

        stock, created = Stock.objects.get_or_create(
            address=address
        )

        for position in positions:
            product_id = position.get(
                'product'
            )

            product = Product.objects.filter(
                id=product_id
            )

            if product.exists():
                stock_product = StockProduct.objects.filter(
                    product_id=product_id,
                    stock=stock
                )

                if not stock_product.exists():
                    StockProduct.objects.create(
                        stock=stock,
                        product_id=product_id,
                        quantity=position.get(
                            'quantity'
                        ),
                        price=position.get(
                            'price'
                        )
                    )

                else:
                    return Response(
                        {"error": "Stock with id {} already have the product with id {}".\
                            format(stock.id, product_id)},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            else:
                return Response(
                    {"error": "Product with id {} does not exist".format(product_id)},
                    status=status.HTTP_400_BAD_REQUEST
                )

        serializer = StockSerializer(
            stock
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )

    def partial_update(self, request, pk=None):
        """
        Используется для частичного обновления объекта Stock
        """
        stock = Stock.objects.filter(
            id=pk
        )

        if stock.exists():
            instance = stock.first()

            positions_data = request.data.get(
                'positions', []
            )

            for position_data in positions_data:
                product_id = position_data.get(
                    'product'
                )
                quantity = position_data.get(
                    'quantity'
                )
                price = position_data.get(
                    'price'
                )

                try:
                    stock_product = StockProduct.objects.get(
                        stock=instance,
                        product_id=product_id
                    )

                    stock_product.quantity = quantity
                    stock_product.price = price
                    stock_product.save()

                except StockProduct.DoesNotExist:
                    StockProduct.objects.create(
                        stock=instance,
                        product_id=product_id,
                        quantity=quantity,
                        price=price
                    )

            serializer = StockSerializer(
                instance
            )

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        else:
            return Response(
                'Stock not found',
                status=status.HTTP_404_NOT_FOUND
            )
