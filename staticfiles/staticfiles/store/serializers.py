from rest_framework import serializers
from .models import Order, OrderItem
from product.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):

    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ('__all__')

class OrderSerializer(serializers.ModelSerializer):

    orderitems = OrderItemSerializer(many=True,read_only=True)

    class Meta:
        model = Order
        exclude = ('session_id', )