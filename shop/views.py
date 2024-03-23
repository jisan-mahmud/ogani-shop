from django.shortcuts import render, redirect
from django.views import View
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from shop.models import Product, CustomerReview
from category.models import Category
from order.models import Order
from .forms import ReviewForm
import ipinfo
import haversine as hs
from haversine import Unit
from django.shortcuts import HttpResponse

class ShopView(View):
    template_name = 'shop/shop.html'
    paginate_by = 10

    def get(self, request, category_slug=None, min_price=0, max_price=0):
        categories = Category.objects.all()
        products = None
        discounted_product = Product.objects.filter(is_available=True, discount__gte=1).order_by('-discount')[:5]
        popular_product = Product.objects.filter(is_available= True).order_by('-views')[:8]
        query = request.GET.get('search_query')

        if query:
            #filter product based on search query
            products = Product.objects.filter(Q(product_name__icontains=query) | Q(description__icontains=query))
        else:
            if category_slug:
                products = Product.objects.filter(category__slug=category_slug, is_available=True)
            else:
                products = Product.objects.filter(is_available=True)
            #filter query based on minimum price and maximum price
            if (min_price < max_price) and (min_price != 0 or max_price != 0):
                products = products.filter(price__gte=min_price, price__lte=max_price)

        #create paginator for products
        items = products.count()
        paginator = Paginator(products, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'products': page_obj,
            'items': items,
            'categories': categories,
            'discounted_product': discounted_product,
            'popular_product': popular_product
        }
        return render(request, self.template_name, context)

class DetailsView(View):
    template_name = 'shop/shop-details.html'
    def get(self, request, product_slug):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        if ip == '127.0.0.1': # Only define the IP if you are testing on localhost.
            ip = '8.8.8.8'

        return HttpResponse(ip)
        # shop_ip = '27.123.253.161'
        # access_token = 'ffe413e672a58f'
        # handler = ipinfo.getHandler(access_token= access_token)
        # details1 = handler.getDetails(shop_ip)
        # details2 = handler.getDetails(user_ip)
        # point1 = details1.loc
        # point2 = details2.loc

        # h = hs.haversine(point1, point2, Unit.KILOMETERS)
        # print(h)


        product = Product.objects.get(slug= product_slug)
        product.views+=1 #increment product view
        product.save()
        #filter related post based on category
        related_products = Product.objects.filter(category__slug= product.category.slug)[:4]
        #Filter review for this single page
        reviews = CustomerReview.objects.filter(product= product)
        #calculate avarage rating and total review
        total_rating = 0
        total_review = reviews.count()
        avarage_rating= 0
        if total_review > 0:
            for review in reviews:
                total_rating += review.rating
            avarage_rating = total_rating / total_review

        #create reviews paginator
        paginator = Paginator(reviews, 1)
        page_number = request.GET.get('page')
        review_obj = paginator.get_page(page_number)
        has_page = review_obj.has_next()

        context = {
            'product': product,
            'reviews': review_obj,
            'related_products': related_products,
            'total_review': total_review,
            'avarage_rating': avarage_rating,
            'has_page': has_page,
            }
        return render(request, self.template_name, context)

    def post(self, request, product_slug):
        #checking user is authenticated
        if request.user.is_authenticated:
            form = ReviewForm(request.POST)
            #check form validation
            if form.is_valid():
                #product extract from Order table
                buy_product = Order.objects.filter(Q(user= request.user) & Q(status= 'Received') & Q(products__slug= product_slug)).exists()
                #product extract from review table
                existing_review = CustomerReview.objects.filter(Q(user=request.user) & Q(product__slug=product_slug)).exists()
                #check user buy this product and user first time review for this product
                if buy_product and not existing_review:
                    instance = form.save(commit= False)
                    instance.user= request.user
                    instance.product = Product.objects.get(slug= product_slug)
                    instance.save()
                    messages.success(request, 'Thanks for your comment!')
                else:
                    messages.error(request, 'You are comment in already or not buy this product!')
            return redirect('product_details', product_slug)
        else:
            return redirect('login')

def contact_view(request):
    return render(request, 'shop/contact.html')