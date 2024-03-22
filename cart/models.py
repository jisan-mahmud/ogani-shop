from django.db import models
from shop.models import Product
from django.contrib.auth.models import User

class Cart(models.Model):
    cart_added = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='cart')

    def __str__(self):
        return str(self.user.username)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete= models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete= models.CASCADE, related_name='cart_items')
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.after_discount() * self.quantity

    def __str__(self):
        return str(self.product)
