from decimal import Decimal
from django.conf import settings
from apps.shop.models import Product
from apps.cart.models import account_data
import json


class Cart(object):

    def __init__(self, request):
        self.request =request 
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        quantity_product = int(quantity)
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity_product
        else:
            self.cart[product_id]['quantity'] += quantity_product
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
        self.setSessionOrAccountData( self.cart)

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):

        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def setSessionOrAccountData(self, value):
        key = self.session.session_key  
        if self.request.user:             
            username = self.request.user
            try:
                record = account_data.objects.get(username=username)
                record.value = value = json.dumps(value)
                record.save()
            except account_data.DoesNotExist:
                record = account_data(username=username,key=key, value=json.dumps(value))
                record.save()
        else:
            self.request.session[key] = value