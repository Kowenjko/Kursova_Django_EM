from django.conf.urls import url
from . import views
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.homepage, name='homepage'),
    url(r'^store/$', views.store, name='store'),
    path('store/<category_slug>/', views.store_by_category,name='store_by_category'),
    path(r'product/<slug:product_slug>', views.product, name='product'),
    url(r'^logout/$', views.log_out, name='log_out'),
  
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
