from django.urls import path
from .views import index, about, add_product, dashboard

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('add-product', add_product, name='add_product'),
    path('dashboard/', dashboard, name='dashboard'),
]