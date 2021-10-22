from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart-detail'),
    path('add/<int:drug_id>/', views.cart_add, name='cart-add'),
    path('remove/<int:drug_id>/', views.cart_remove, name='cart-remove'),
]