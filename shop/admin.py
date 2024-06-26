from django.contrib import admin
from .models import Product, ShopInfo, CustomerReview
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_name', )}
    list_display = ['product_name', 'price', 'is_available']

admin.site.register(Product, ProductAdmin)
admin.site.register(ShopInfo)
admin.site.register(CustomerReview)