from django.urls import path
from .views import ShopView, DetailsView, contact_view
urlpatterns = [
    path('', ShopView.as_view(), name= 'shop'),
    path('<slug:category_slug>/', ShopView.as_view(), name='category'),
    path('price_range/<int:min_price>/<int:max_price>/', ShopView.as_view(), name='price_range'),
    path('product_details/<slug:product_slug>/' , DetailsView.as_view(), name= 'product_details'),
    path('contact' , contact_view, name= 'contact'),
]
