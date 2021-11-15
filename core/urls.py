# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include  # add this

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
     path('shop/', include(("apps.shop.urls",'shop'),namespace='shop')),             
    path('cart/', include(("apps.cart.urls","cart"),namespace='cart')),             
    path('orders/', include(("apps.orders.urls","orders"),namespace='orders')), 
   
    path('admin/', admin.site.urls),          # Django admin route
    path("", include("apps.authentication.urls")),
     path("", include(("apps.home.urls","home"),namespace='home')), # Auth routes - login / register
              # UI Kits Html files 
                  
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += staticfiles_urlpatterns()