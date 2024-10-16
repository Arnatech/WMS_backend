from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductList,
    CategoryList,
    Product_detail,
    Product_category,
    CartViewSet,
    OrderViewSet
)

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('products/', ProductList, name='product-list'),
    path('categories/', CategoryList, name='category-list'),
    path('products/<str:product_name>/', Product_detail, name='product-detail'),
    path('products/category/<str:category_name>/', Product_category, name='product-category'),
    path('', include(router.urls)),
]
