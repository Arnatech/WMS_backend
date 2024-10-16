from django.db import models
from users.models import User
from cloudinary.models import CloudinaryField
import uuid

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField()

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name



class Product(models.Model):
    id = models.UUIDField(primary_key=True,  default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=40, unique=True)
    image = CloudinaryField('image')
    brand = models.CharField(max_length=30)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)

    def __str__(self):
        return f"Cart for {self.user.username}"

    def total_price(self):
        return sum(item.product.selling_price * item.quantity for item in self.items.all())


class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    def total_price(self):
        return sum(item.product.selling_price * item.quantity for item in self.items.all())



