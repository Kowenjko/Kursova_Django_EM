from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    url(r'^checkout/$', views.checkout, name='checkout'),
    path('detail/<int:pk>/', views.detail, name='detail'),
    url(r'^orders/$', views.orders, name='orders'),

]
