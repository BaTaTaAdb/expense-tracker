from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image_url = models.URLField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    url = models.URLField(max_length=2083)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    purchased_at = models.DateTimeField(blank=True)
    
    def __str__(self) -> str:
        return self.name
    

class Courier(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image_url = models.URLField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='couriers/', blank=True, null=True)
    url = models.URLField(max_length=2083)
    
    def __str__(self) -> str:
        return self.name
    

class OrderDelivery(models.Model):
    ORDER_STATUS_CHOICES = [
    ('Processing', 'Processing'),
    ('In-Transit', 'In-Transit'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),
    ('Returned', 'Returned'),
    ('Refunded', 'Refunded'),
    ('Failed', 'Failed'),
    ('Delayed', 'Delayed'),
    ]
    
    order_status = models.CharField(
        max_length=10,
        choices=ORDER_STATUS_CHOICES,
        default='Processing',
    )
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f"Delivery #{self.pk} by {self.courier.name} - {self.order_status}"
    
class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.quantity}x '{self.product.name}' of Order #{self.order.pk} from {self.order.user.first_name} (#{self.order.user.pk})"

class Order(models.Model):
    STATUS_CHOICES = [
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_items = models.ManyToManyField(Product, through=OrderItem)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Processing')
    delivery = models.OneToOneField(OrderDelivery, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        first_name = self.user.first_name or "User"
        return "{}'s order - #{}".format(first_name, self.pk)
    