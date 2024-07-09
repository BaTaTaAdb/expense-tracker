from django.contrib import admin

# Register your models here.
from .models import Product, Courier, Order, OrderDelivery

admin.site.register(Product)
admin.site.register(Courier)
admin.site.register(Order)
admin.site.register(OrderDelivery)
