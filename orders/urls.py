"""pyshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'^basket_adding/$', views.basket_adding, name='basket_adding'),
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^delete_item_in_basket/(?P<product_id>\w+)/$', views.delete_item_in_basket, name='delete_item_in_basket'),
    url(r'^cart/$',views.cart, name='cart'),
    url(r'^basket_top/$',views.basket_top, name='basket_top'),
    url(r'^add_to_cart/(?P<product_id>\w+)/$',views.add_to_cart, name='add_to_cart'),
    url(r'^add_to_cart_wishlist/(?P<product_id>\w+)/$',views.add_to_cart_wishlist, name='add_to_cart_wishlist'),
]
