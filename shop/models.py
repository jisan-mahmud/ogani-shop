from collections.abc import Iterable
from django.db import models
from category.models import Category
from decimal import Decimal
from django.contrib.auth.models import User
# Create your models here.

#product details model
class Product(models.Model):
    product_name = models.CharField(max_length= 40, unique= True)
    slug = models.CharField(max_length= 80)
    description = models.CharField(max_length= 500)
    price = models.DecimalField(decimal_places= 2, max_digits= 12)
    weight = models.DecimalField(max_digits= 5,decimal_places= 2)
    unit = models.CharField(max_length= 10, default= 'kg')
    discount = models.DecimalField(decimal_places= 2, max_digits= 12, blank= True, default= 0) #store discount percentage
    image = models.ImageField(upload_to= 'photos/product')
    stock = models.IntegerField()
    is_available = models.BooleanField(default= True)
    shipping = models.IntegerField(default= 1, blank= True)
    category = models.ForeignKey(Category, on_delete= models.CASCADE, related_name= 'product')
    views = models.IntegerField(default= 0, blank= True)
    created_date = models.DateTimeField(auto_now= True)
    modified_date = models.DateTimeField(auto_now_add= True)


    def after_discount(self):
        if self.discount > 0:
            discounted_price = self.price * (1 - self.discount / 100)
            return Decimal(discounted_price).quantize(Decimal('0.00'))
        else:
            return Decimal(self.price).quantize(Decimal('0.00'))


    def __str__(self):
        return self.product_name



class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Override save method to ensure only one instance exists
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

#shop information
class ShopInfo(SingletonModel):
    shop_name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email_address = models.EmailField(max_length=50)
    about = models.TextField(blank=True, null=True)
    fb_page = models.URLField(max_length=200, blank=True)
    instagram = models.URLField(max_length=200, blank=True)
    twitter = models.URLField(max_length=200, blank=True)
    offer = models.CharField(max_length= 100)

class CustomerReview(models.Model):
    rating = models.IntegerField()
    review = models.TextField()
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    product = models.ForeignKey(Product, on_delete= models.CASCADE)
    date_time = models.DateTimeField(auto_now_add= True)

    class Meta:
        # Ensure that each user can only submit one review per product
        unique_together = ('user', 'product')

    def __str__(self):
        return f'Rating {self.rating} by {self.user.first_name}'
