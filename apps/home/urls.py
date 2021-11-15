# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path("update-product/<slug:slug>/", views.update_product, name='update_product'),
    path("delete-product/<slug:slug>/", views.product_delete, name='product_delete'),
    path("change-status/<int:id>/", views.change_status, name='change_status'),
  
    
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),
    
    

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()