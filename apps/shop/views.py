from django.shortcuts import render, get_object_or_404
from .models import Product, Brand, Category
from apps.cart.forms import CartAddProductForm
from apps.cart.cart import Cart
from django.conf import settings
from django.core.paginator import Paginator
# Create your views here.
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import  logout

ITEMS_PER_PAGE = 6


class ProductList(ListView):
    paginate_by = 3
    model = Product


def homepage(request):
    return render(request, 'electro/pages/index.html', {'cart': cart(request),
                                                        'count': count(request)})


def store(request, category_slug=None):   

    category = None
    categories = Category.objects.all()
    brand = None
    brands = Brand.objects.all()
    category_id_list = []
    brand_id_list = []

    for item in categories:      
        if request.POST.get(f'category-{item.id}', False) == 'on':
            category_id_list.append(item.id)

    for item in brands:
        if request.POST.get(f'brand-{item.id}', False) == 'on':
            brand_id_list.append(item.id)

    if category_id_list and brand_id_list:
        products = Product.objects.filter(
            available=True, category__in=category_id_list, brand__in=brand_id_list)
    elif category_id_list:
        products = Product.objects.filter(
            available=True, category__in=category_id_list)
    elif brand_id_list:
        products = Product.objects.filter(
            available=True,  brand__in=brand_id_list)

    else:
        products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    cart_product_form = CartAddProductForm()
    cart_items = request.session.get(settings.CART_SESSION_ID)
    pr = []
    if cart_items:
        product = cart_items.keys()
        pr = Product.objects.filter(id__in=product)
    count_page = len(products)
    # Show 25 contacts per page.
    paginator = Paginator(products, ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'electro/pages/store.html', {'category': category,
                                                'brands': brands,
                                                'categories': categories,
                                                'products': products,
                                                'cart_product_form': cart_product_form,
                                                'cart': cart(request),
                                                'cart_items': pr,
                                                'count': count(request),
                                                'category_id_list': category_id_list,
                                                'brand_id_list': brand_id_list,
                                                'count_page': count_page,
                                                'page_obj': page_obj,
                                                'ITEMS_PER_PAGE': ITEMS_PER_PAGE
                                                })


def store_by_category(request, category_slug=None):
    category = None
    categories = Category.objects.all()

    brand = None
    brands = Brand.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    cart_product_form = CartAddProductForm()
    cart_items = request.session.get(settings.CART_SESSION_ID)
    pr = []
    if cart_items:
        product = cart_items.keys()
        # pr = Product.objects.filter(id__in=product)
    paginator = Paginator(products, ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'electro/pages/store.html', {'category': category,
                                                'categories': categories,
                                                'products': products,
                                                'cart_product_form': cart_product_form,
                                                'cart': cart(request),
                                                # 'cart_items': pr,
                                                'count': count(request),
                                                'page_obj': page_obj,
                                                'ITEMS_PER_PAGE': ITEMS_PER_PAGE
                                                })


def product(request,  product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    cart_product_form = CartAddProductForm()
    category = get_object_or_404(Category, slug=product.category.slug)
    return render(request, 'electro/pages/product.html', {'product': product,
                                                  'category': category,
                                                  'cart_product_form': cart_product_form,
                                                  'cart': cart(request),
                                                  'count': count(request),
                                                  })


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

def log_out(request):    
    logout(request)
    return redirect('shop:homepage')
   
