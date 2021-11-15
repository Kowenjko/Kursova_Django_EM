from django.shortcuts import render, get_object_or_404


from .models import OrderItem
from .forms import OrderCreateForm
from apps.cart.cart import Cart
from apps.shop.models import Product
from .models import Order
from django.conf import settings
from apps.cart.models import account_data


def checkout(request):
    cart_user = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            order.username = request.user
            order.save()

            for item in cart_user:
                OrderItem.objects.create(
                    username=request.user,
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'])
            cart_user.clear()
            deleteSessionOrAccountData(request)
            return render(request, 'order/created.html', {'order': order})
    else:
        form = OrderCreateForm
    return render(request, 'electro/pages/checkout.html',
                  {'cart': cart(request), 'form': form, 'count': count(request), })


def deleteSessionOrAccountData(request):
    if request.user:
        username = request.user
        account_data.objects.filter(username=username).delete()


def detail(request, pk):
    orderItems = OrderItem.objects.filter(order_id=pk)
    subtotal = 0
    countOrder = 0
    if orderItems:
        for item in orderItems:
            countOrder += item.quantity
            subtotal += item.quantity*item.price
    return render(request, 'order/detail.html', {'orderItems': orderItems, 'pk': pk, 'cart': cart(request), 'subtotal': subtotal, 'countOrder': countOrder, 'count': count(request)})


def orders(request):
    username = request.user
    order = Order.objects.filter(username=username)
    subtotal = 0
    countOrder = 0
    if order:
        for itemOrder in order:
            orderItems = OrderItem.objects.filter(order_id=itemOrder.id)
            for item in orderItems:
                countOrder += item.quantity
                subtotal += item.quantity*item.price
    return render(request, 'order/orders.html', {'orders': order, 'cart': cart(request), 'subtotal': subtotal, 'countOrder': countOrder, 'count': count(request)})


def count(request):
    cart = request.session.get(settings.CART_SESSION_ID)
    count = 0
    if cart:
        cart_values = cart.values()
        for item in cart_values:
            count += item['quantity']
    return count


def cart(request):
    cart = request.session.get(settings.CART_SESSION_ID)
    count = 0
    subtotal = 0
    product_list = []
    if cart:
        cart_values = cart.values()
        for item in cart_values:
            count += item['quantity']
            subtotal += item['quantity']*float(item['price'])
        cart_items_id = cart.keys()
        product_list = Product.objects.filter(id__in=cart_items_id)

    return {'count': count, 'product_list': product_list, 'cart': cart, 'subtotal': subtotal}
