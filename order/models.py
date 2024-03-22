from django.db import models
from django.contrib.auth.models import User
from shop.models import Product

class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Complete', 'complete'),
        ('Received', 'Received')
    )
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    products = models.ManyToManyField(Product)
    first_name = models.CharField(max_length= 50)
    last_name = models.CharField(max_length= 50)
    order_date = models.DateTimeField(auto_now_add= True)
    total_amount = models.DecimalField(max_digits= 12, decimal_places= 2)
    address = models.TextField()
    city = models.CharField(max_length= 100)
    postal_code = models.CharField(max_length= 20)
    phone_number = models.TextField(max_length= 15)
    email_address = models.EmailField(max_length= 50)
    note = models.TextField(max_length= 200, blank= True)
    status = models.CharField(max_length= 10, choices= STATUS, default= 'New')
    payment_method = models.CharField(max_length= 20)

    def __str__(self):
        return f"Order #{self.pk} by {self.user.username}"
