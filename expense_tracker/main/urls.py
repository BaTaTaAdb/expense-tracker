from django.urls import path
from .views import (
    index, about, add_product, dashboard, 
    order_details, product_details, order_item_details,
    create_order_single_item, order_success,
    delete_order)

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('add-product', add_product, name='add_product'),
    path('dashboard/', dashboard, name='dashboard'),
    path('order/<int:pk>/', order_details, name='order_details'),
    path('product/<int:pk>/', product_details, name='product_details'),
    path('order-item/<int:pk>/', order_item_details, name='order_item_details'),
    path('create-order/single-item', create_order_single_item, name='create_order_single_item'),
    path('create-order/success/<int:pk>/', order_success, name='order_success'),
    path('order/<int:pk>/delete/', delete_order, name='delete_order'),
]