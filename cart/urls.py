from django.urls import path
from . import views

urlpatterns = [
   path('', views.CartView.as_view(), name= 'cart'),
   path('added_cart/<int:id>', views.added_cart, name= 'added_cart'),
   path('decrease_cart/<int:pk>', views.decrease_cart, name= 'decrease_cart'),
   path('remove_cart/<int:id>', views.remove_cart , name= 'remove_cart'),
]
