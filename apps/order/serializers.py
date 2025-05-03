from rest_framework import serializers

from apps.order.models import Order, OrderItem


class OrderBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderCreateSerializer(serializers.Serializer):
    seat_ids = serializers.ListField()
    movie_schedule_id = serializers.IntegerField()


class OrderItemBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderItemListSerializer(serializers.ModelSerializer):
    order_serial = serializers.SerializerMethodField()
    product_info = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ('order_serial', 'product_info', 'number_of_product', 'price', 'total_price', 'modified_time', 'created_time')

    @staticmethod
    def get_order_serial(obj):
        return obj.order.serial

    @staticmethod
    def get_product_info(obj):
        return dict(
            title=obj.product.title,
            price=obj.product.price
        )

    @staticmethod
    def get_total_price(obj):
        return obj.product.price * obj.number_of_product
