from .serializers import CategorySerializer, ProductSerializer, CartSerializer, OrderSerializer, CartItemSerializer, OrderItemSerializer
from .models import Product, Category, Cart, CartItem, Order, OrderItem
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action

# Create your views here.
@api_view(['GET'])
def ProductList(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

@api_view(['GET'])   
def CategoryList(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    

@api_view(['GET'])
def Product_detail(request, product_name):
    if request.method == 'GET':
        try:
            product = Product.objects.get(name=product_name)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)
        
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    

@api_view(['GET'])
def Product_category(request, category_name):
    if request.method == 'GET':
        try:
            products = Product.objects.get(Category=category_name)
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=404)
        serializer = ProductSerializer(products)
        return Response(serializer.data)


class CartViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        product = Product.objects.get(id=product_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['put'])
    def update_item(self, request, pk=None):
        cart_item = CartItem.objects.get(id=pk)
        quantity = request.data.get('quantity')

        if quantity:
            cart_item.quantity = quantity
            cart_item.save()
            serializer = CartItemSerializer(cart_item)
            return Response(serializer.data)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'])
    def remove_item(self, request, pk=None):
        cart_item = CartItem.objects.get(id=pk)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['delete'])
    def clear_cart(self, request):
        cart = Cart.objects.get(user=request.user)
        cart.items.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        cart = Cart.objects.get(user=request.user)
        order = Order.objects.create(user=request.user)

        for item in cart.items.all():
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)

        # Clear the cart after checkout
        cart.items.all().delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        order = Order.objects.get(id=pk, user=request.user)
        serializer = OrderSerializer(order)
        return Response(serializer.data)