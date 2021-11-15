from django.db import models
from apps.shop.models import Product
from django.contrib.auth.models import User


class Order(models.Model):
    username = models.ForeignKey(User,  null=True, blank=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    status = models.CharField(max_length=20,choices=[('progress','In Progress'),('accepted','Accepted'),('shipped','Shipped'),('completed','Completed')], default="In Progress")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)


    class Meta:
        ordering = ('-created',)
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    username = models.ForeignKey(
        User,  null=True, blank=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(
        Order, related_name='products', null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(
        Product, related_name='products', null=True, on_delete=models.SET_NULL)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
