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
    url(r'^$', views.home, name='home'),
    url(r'^landing', views.landing, name='landing'),
    url(r'^login', views.login_view, name='login_view'),
    url(r'^logout', views.logout_view, name='logout_view'),
    url(r'^register', views.register, name='register'),
    url(r'^account', views.account, name='account'),
    url(r'^order', views.order, name='order'),
    url(r'^productview', views.productview, name='productview'),
    url(r'^wishlist', views.wishlist, name='wishlist'),
    url(r'^delete_item_in_wishlist/(?P<product_id>\w+)/$',views.delete_item_in_wishlist, name='delete_item_in_wishlist'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]
