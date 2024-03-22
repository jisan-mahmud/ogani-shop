from django.urls import path
from . import views

urlpatterns = [
   path('profile/', views.profile, name= 'profile'),
   path('receive/', views.received_view, name= 'receive'),
   path('register/', views.register, name= 'register'),
   path('login/', views.user_login, name= 'login'),
   path('active/<uid>/<token>', views.activated, name= 'activated'),
   path('logout/', views.user_logout, name= 'logout'),
   path('change-password/', views.change_password, name= 'change_password')
]
