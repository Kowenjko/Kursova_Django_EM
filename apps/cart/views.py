from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from apps.shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from apps.cart.models import account_data
import json
from django.conf import settings

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)

    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid:
        cd = request.POST
        # cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'],
                 update_quantity=cd['update'])
        count = cart.__len__()
        key = request.session.session_key       
        # setSessionOrAccountData(request, key, cart)
        # cart.add(product=product, quantity=form['quantity'],
        #          update_quantity=form['update'])

    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)  
    print(settings.MEDIA_URL)
    print(settings.MEDIA_ROOT)
    return render(request, 'electro/cart/detail.html', {'cart': cart, 'count': cart.__len__()})

