from django.urls import path
from .views import index, about, add_product, dashboard, order_details, product_detail

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('add-product', add_product, name='add_product'),
    path('dashboard/', dashboard, name='dashboard'),
    path('order/<int:pk>/', order_details, name='order_details'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
]