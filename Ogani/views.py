from django.shortcuts import render
from shop.models import Product
def home(request):
    products = Product.objects.filter(is_available= True)[:10]
    return render(request, 'index.html', {'products': products})