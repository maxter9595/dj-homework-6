from rest_framework import serializers

from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели для продукта
    """
    class Meta:
        model = Product
        fields = '__all__'


class ProductPositionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для позиции продукта на складе
    """
    class Meta:
        model = StockProduct
        fields = [
            'product',
            'quantity',
            'price'
        ]


class StockSerializer(serializers.ModelSerializer):
    """
    Сериализатор для склада
    """
    positions = ProductPositionSerializer(
        many=True
    )

    class Meta:
        model = Stock
        fields = '__all__'

    def create(self, validated_data):
        """
        Используется для модификации метода create
        при работе с моделью Stock (основная логика +
        заполнение данных модели StockProduct)
        """
        positions_data = validated_data.pop(
            'positions'
        )

        # Добавляем склад в таблицу со складами (основная логика)
        stock = super().create(
            validated_data
        )

        # Добавление товаров в связующую таблицу (дополнительная логика)
        for position_data in positions_data:
            StockProduct.objects.create(
                stock=stock,
                **position_data
            )

        return stock

    def update(self, instance, validated_data):
        """
        Используется для модификации метода update
        при работе с моделью Stock (основная логика +
        обновление данных модели StockProduct)
        """
        positions_data = validated_data.pop(
            'positions'
        )

        # Обновление склада в таблице со складами (основная логика)
        stock = super().update(
            instance,
            validated_data
        )

        # Обновление данных по товарам в связующей таблице (дополнительная логика)
        for position_data in positions_data:
            obj, created = StockProduct.objects.update_or_create(
                stock=stock,
                product=position_data.get('product'),
                defaults={
                    'stock': stock,
                    'product': position_data.get('product'),
                    'quantity': position_data.get('quantity'),
                    'price': position_data.get('price')
                }
            )

        return stock
