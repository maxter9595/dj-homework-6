from rest_framework import serializers

from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Product
    """
    class Meta:
        model = Product
        fields = '__all__'


class ProductPositionSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели StockProduct
    """
    class Meta:
        model = StockProduct
        fields = '__all__'


class StockSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Stock
    """
    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    positions = ProductPositionSerializer(
        many=True
    )

    def create(self, validated_data):
        """
        Используется для создания нового экземпляра модели Stock
        """
        positions_data = validated_data.pop(
            'positions'
        )

        stock = Stock.objects.create(
            **validated_data
        )

        for position_data in positions_data:
            StockProduct.objects.create(
                stock=stock,
                **position_data
            )

        return stock

    def update(self, instance, validated_data):
        """
        Используется для обновления существующего экземпляра модели Stock
        """
        positions = instance.positions.all()
        positions = list(positions)

        positions_data = validated_data.pop(
            'positions'
        )

        instance.address = validated_data.get(
            'address',
            instance.address
        )
        instance.save()

        for position_data in positions_data:
            position = positions.pop(0)

            position.product = position_data.get(
                'product',
                position.product
            )

            position.quantity = position_data.get(
                'quantity',
                position.quantity
            )

            position.price = position_data.get(
                'price',
                position.price
            )
            position.save()

        return instance
