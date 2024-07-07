from rest_framework import filters, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from logistic.serializers import ProductSerializer, StockSerializer

from logistic.models import Product, Stock, StockProduct


class ProductViewSet(ModelViewSet):
    """
    ViewSet модели Product
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [
        filters.SearchFilter
    ]

    search_fields = [
        'title',
        'description'
    ]

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
        filters.SearchFilter
    ]

    search_fields = [
        'address'
    ]

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
            StockProduct.objects.create(
                stock=stock,
                product_id=position.get(
                    'product'
                ),
                quantity=position.get(
                    'quantity'
                ),
                price=position.get(
                    'price'
                )
            )

        serializer = StockSerializer(
            stock
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )

    def partial_update(self, request, *args, **kwargs):
        """
        Используется для частичного обновления объекта Stock
        """
        instance = self.get_object()
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

    def list(self, request, *args, **kwargs):
        """
        Возвращает список объектов Stock, отфильтрованный по одному из двух вариантов:
        - по параметру products__id (если указан параметр ?products=... в GET-запросе)
        - по названию или описанию продукта (если указан параметр ?search=... в GET-запросе)
        """
        product_id = request.query_params.get(
            'products',
        )

        product_query = request.query_params.get(
            'search',
        )

        if product_id:
            stocks = Stock.objects.filter(
                products__id=product_id
            )

        elif product_query:
            stocks = Stock.objects.filter(
                positions__product__title__icontains=product_query
            ) | Stock.objects.filter(
                positions__product__description__icontains=product_query
            )

        else:
            return super().list(request, *args, **kwargs)

        serializer = StockSerializer(
            stocks,
            many=True
        )

        return Response(
            serializer.data
        )
