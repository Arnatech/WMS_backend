from rest_framework import serializers
from .models import Product, Category, Cart, CartItem, Order, OrderItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'brand', 'description', 'selling_price', 'image']


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

        def get_total_price(self, obj):
            return obj.total_price()


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'get_total_cost']


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'total_price']

        def get_total_price(self, obj):
            return obj.total_price()


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'ordered_at', 'items', 'total_cost']