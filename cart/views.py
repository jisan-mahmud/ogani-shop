from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from shop.models import Product
from .models import Cart, CartItem
# Create your views here.
def create_cart(user):
    cart = Cart.objects.create(user= user)
    cart.save()

class CartView(View):
    template_name = 'cart/shoping-cart.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            cart = Cart.objects.get(user= request.user)
            cart_items = CartItem.objects.filter(cart= cart)
            delivery_charge = 80;
            sub_total = 0;
            total_price = 0;
            for item in cart_items:
                sub_total += item.sub_total()
            total_price = sub_total + delivery_charge

            context = {
                'cart_items': cart_items,
                'sub_total': sub_total,
                'delivery_charge': delivery_charge,
                'total_price': total_price
            }
            return render(request, self.template_name,context)
        else:
            return redirect('login')

def added_cart(request, id):
    if request.user.is_authenticated:
        product = Product.objects.get(id= id)
        try:
            user_cart = Cart.objects.filter(user= request.user)
            if user_cart.exists():
                user_cart = user_cart[0]
            else:
                user_cart = create_cart(request.user)
            cart_item = CartItem.objects.filter(cart= user_cart, product= product)[0]
            if cart_item:
                cart_item.quantity += 1
                cart_item.save()
        except:
            cart_item = CartItem.objects.create(
                cart= user_cart,
                product= product,
                quantity=1
                )
            cart_item.save()
        return redirect('cart')
    else:
        return redirect('login')
def decrease_cart(request, pk):
    product = Product.objects.get(id= pk)
    try:
        cart = get_object_or_404(Cart, user= request.user)
        cart_item = CartItem.objects.filter(cart= cart, product= product)[0]
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart(request, id):
    try:
        cart_item = CartItem.objects.get(id= id)
        if cart_item:
            cart_item.delete()
    except:
        pass
    return redirect('cart')
