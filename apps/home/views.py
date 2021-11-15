from django.contrib.auth.models import User
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.conf import settings
from django.shortcuts import render,redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from pprint import pprint
from operator import itemgetter

from django.template.defaultfilters import slugify
from apps.shop.models import Brand, Category, Product
from apps.orders.models import OrderItem,Order
from . forms import ProductForm, CategoryForm, BrandForm



@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'home:index'}
    context['total']=total_index(request)

    html_template = loader.get_template('home/index_main.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]      
        
       
        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        if load_template=='tables-product.html':
            products = Product.objects.filter(available=True)
            context['products']=products
        
        

        if load_template=='add_product.html':
            # er=''
            form = ProductForm()
            form_category = CategoryForm()
            form_brand = BrandForm()            
            context['form']=form
            context['form_category']=form_category
            context['form_brand']=form_brand

            if 'formCategory' in request.POST:
                 add_category(request) 

            if 'formProduct' in request.POST:
                 add_product(request)  

            if 'formBrand' in request.POST:
                 add_brand(request)        

        if load_template=='tables-orders.html':
            context['orders']=orders(request)
       
        if load_template=='index_main.html':
            context['total']=total_index(request)

          
            
                      
        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


    

def orders(request):    
    order = Order.objects.all()
    subtotal = 0
    countOrder = 0
    top={}
    user_list=[]    
    if order:
        
        for itemOrder in order:
            user_order={}
            usertotal = 0
            usercount = 0
            orderItems = OrderItem.objects.filter(order_id=itemOrder.id)
            orderUsers=OrderItem.objects.filter(username=itemOrder.username,order_id=itemOrder.id)            
            for item in orderUsers:
                usercount += item.quantity
                usertotal += item.quantity*item.price
            for item in orderItems:
                list_keys=list(top)
                list_product=[]
                if item.product.name in  list_keys:                   
                    list_product.append( top[item.product.name][0]+item.quantity)
                    list_product.append(item.price)
                    top[item.product.name] =list_product
                else:
                    list_product.append(item.quantity)
                    list_product.append(item.price)
                    top[item.product.name]=list_product
                countOrder += item.quantity
                subtotal += item.quantity*item.price
                        
            user_order['orderUsers']=orderUsers
            user_order['count']=usercount
            user_order['total']=usertotal
            user_order['id']=itemOrder.id
            user_list.append(user_order) 
    list_top=[]
    for item in top.items():
        end_top={
            'name':item[0],
            'quantity':item[1][0],
            'price':item[1][1],
            'total_price':item[1][0]*item[1][1]
        }
        list_top.append(end_top)         
    all_orders={
        'user_order':user_list,
        'orders': order,
        'top':list_top,        
        'subtotal': subtotal,
        'countOrder': countOrder, 
        
    }
    return all_orders



def total_index(request):    
    products=Product.objects.all()    
    order = orders(request)
    user=User.objects.all()   
    # print(order['top'])
    sorted_top=sorted(order['top'], key=itemgetter('quantity'),reverse=True)
    linght=len(sorted_top)
    if linght>6: linght=6    
    list_name=[ sorted_top[item]['name'] for item in range(linght) ]
    list_quantity=[sorted_top[item]['quantity'] for item in range(linght) ]
    print(list_name)      
    stock=0
    for product in products:
        stock +=product.stock
    total={
        'products':products,
        'orders':order,  
        'sorted_top':sorted_top,  
        'top_name':list_name,    
        'top_quantity':list_quantity,    
        'stock_product':stock,
        'procent':round(order['countOrder']*100/stock),
        'count_user':len(user)-1
    }
    return total    
   

@require_http_methods(['POST'])
def change_status(request, id):
    order_status=Order.objects.filter(id=id)
    status=['In Progress','Accepted','Shipped','Completed']    
    index=status.index(order_status[0].status)
    if len(status)-1 <= index:
        index=0
    else:
          index+=1
    context={}
    order_status.update(status=status[index])
    context = {'segment': 'tables-orders.html'} 
    context['orders']=orders(request)
    html_template = loader.get_template('home/tables-orders.html')    
    return HttpResponse(html_template.render(context, request))



def add_product(request):    
    if request.method=='POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():                    
            response=form.save(commit=False)            
            response.slug = slugify(response.name)                    
            response.save() 
            return redirect('home:pages')         
        return 'Не коректні дані'   




def update_product(request,slug):   
    product = get_object_or_404(Product, slug=slug)    
    products = Product.objects.filter(available=True)  
    if request.method=='POST':
        form = ProductForm(request.POST,request.FILES,instance=product)
        if form.is_valid():                    
            response=form.save(commit=False)            
            response.slug = slugify(response.name)                    
            response.save() 
            return redirect('home:pages')        
        return 'Не коректні дані'
    else:
        form = ProductForm(instance=product)    
    context = {'segment': 'edit_product.html'} 
    context['products']=products  
    context['form']=form    
    html_template = loader.get_template('home/edit_product.html')
    return HttpResponse(html_template.render(context, request))   

def product_delete(request,slug):
    form = ProductForm()       
    products = Product.objects.filter(available=True)    
    product = Product.objects.get(slug=slug)
    product.delete()
    context = {'segment': 'tables-product.html'}
    context['products']=products  
    context['form']=form 
    if 'formProduct' in request.POST:
                 add_product(request)   
    html_template = loader.get_template('home/tables-product.html')
    return HttpResponse(html_template.render(context, request))

def add_category(request):    
    if request.method=='POST':
        form_category = CategoryForm(request.POST)        
        if form_category.is_valid():                      
            response=form_category.save(commit=False)            
            response.slug = slugify(response.name)
            response.save()            
            return redirect('home:pages')       
        return 'Не коректні дані'



def add_brand(request):    
    if request.method=='POST':
        form_brand = BrandForm(request.POST)        
        if form_brand.is_valid():
            response=form_brand.save(commit=False)                 
            response.slug = slugify(response.name)                    
            response.save()            
            return redirect('home:pages')        
        return 'Не коректні дані'

#


 