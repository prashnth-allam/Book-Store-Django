from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

# Create your models here.

class Book(models.Model):
    title=models.CharField(max_length=100)
    author=models.CharField(max_length=100)
    isbn=models.CharField(max_length=20)
    genre=models.CharField(max_length=50)
    price=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Genre(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.book.title} in {self.cart.user.username}'s Cart"

    @property
    def total_price(self):
        return self.book.price * self.quantity

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    shipping_address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Order #{self.pk} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.title} in Order #{self.order.pk}"

    @property
    def total_price(self):
        return self.price * self.quantity