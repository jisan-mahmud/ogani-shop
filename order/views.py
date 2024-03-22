from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import OrderForm
from cart.models import Cart, CartItem

def order_view(request):
    context = {}

    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        if cart_items.exists() == False:
            return redirect('shop')
        delivery_charge = 80
        sub_total = 0
        total_price = 0

        for item in cart_items:
            sub_total += item.sub_total()

        total_price = sub_total + delivery_charge

        context = {
            'items': cart_items,
            'sub_total': sub_total,
            'delivery_charge': delivery_charge,
            'total_price': total_price
        }

        if request.method == "POST":
            form = OrderForm(request.POST)
            form.user = request.user
            if form.is_valid():
                instance = form.save(commit= False)
                instance.total_amount= total_price
                instance.user= request.user
                instance.save()
                instance.payment_method = 'Cash On Delivery'
                #add ordered product in order object
                for item in cart_items:
                    instance.products.add(item.product)
                instance.save()

                #delete cart item after confirm order
                cart_items.delete()

        else:
            form = OrderForm()

    context['form'] = form
    return render(request, 'order/checkout.html', context)
