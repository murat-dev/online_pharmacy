from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from main.models import Drug
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, drug_id):
    cart = Cart(request)
    drug = get_object_or_404(Drug, id=drug_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cleaned_data = form.cleaned_data
        cart.add(drug=drug,
                 quantity=cleaned_data['quantity'],
                 update_quantity=cleaned_data['update'])
    return redirect('cart:cart-detail')


def cart_remove(request, drug_id):
    cart = Cart(request)
    drug = get_object_or_404(Drug, id=drug_id)
    cart.remove(drug)
    return redirect('cart:cart-detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'update': True})
    return render(request, 'cart/detail.html', {'cart': cart})
