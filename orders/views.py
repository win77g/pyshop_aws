from django.shortcuts import render
from django.http import JsonResponse
from .models import *
# from .models import ProductInBasket
from .forms import CheckoutContactForm
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.
def basket_adding(request):
    return_dict = dict()
    session_key = request.session.session_key
    print (request.POST)
    print ('iam from ')
    data = request.POST
    product_id = data.get("product_id")
    nmb = data.get("nmb")

    new_product, created = ProductInBasket.objects.get_or_create(session_key=session_key,product_id=product_id,defaults={"nmb":nmb})
    if not created:
        print ("not created")
        new_product.nmb += int(nmb)
        new_product.save(force_update=True)
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True)
    products_total_nmb = products_in_basket.count()
    # cart_nmb = products_in_basket.nmb.count()
     # products_total_nmb = ProductInBasket.objects.filter(session_key=session_key, is_active=True).count()
    return_dict["products_total_nmb"] = products_total_nmb
    # return_dict["cart_nmb"] = cart_nmb
    return_dict["products"] = list()

    for item in products_in_basket:
        product_dict = dict()
        product_dict["name"] = item.product.name
        product_dict["price_per_item"] = item.price_per_item
        product_dict["nmb"] = item.nmb
        return_dict["products"].append(product_dict)

    cart_total_price = 0
    for product_in_basket in products_in_basket:
        cart_total_price += product_in_basket.total_price
    return_dict["cart_total_price"] = cart_total_price

    cart_nmb = 0
    for product_in_basket in products_in_basket:
        cart_nmb += product_in_basket.nmb
    return_dict["cart_nmb"] = cart_nmb

    # return JsonResponse(return_dict)
    return render(request, 'modal.html', locals())

# для верхней корзины
def basket_top(request):
    return_dict = dict()
    session_key = request.session.session_key
    print (request.POST)
    data = request.POST
    # product_id = data.get("product_id")
    # nmb = data.get("nmb")

    # new_product, created = ProductInBasket.objects.get_or_create(session_key=session_key,product_id=product_id,defaults={"nmb":nmb})
    # if not created:
    #     print ("not created")
    #     new_product.nmb += int(nmb)
    #     new_product.save(force_update=True)
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True)
    products_total_nmb = products_in_basket.count()
    # cart_nmb = products_in_basket.nmb.count()
     # products_total_nmb = ProductInBasket.objects.filter(session_key=session_key, is_active=True).count()
    return_dict["products_total_nmb"] = products_total_nmb
    # return_dict["cart_nmb"] = cart_nmb
    return_dict["products"] = list()

    for item in products_in_basket:
        product_dict = dict()
        product_dict["name"] = item.product.name
        product_dict["price_per_item"] = item.price_per_item
        product_dict["nmb"] = item.nmb
        return_dict["products"].append(product_dict)

    cart_total_price = 0
    for product_in_basket in products_in_basket:
        cart_total_price += product_in_basket.total_price
    return_dict["cart_total_price"] = cart_total_price

    cart_nmb = 0
    for product_in_basket in products_in_basket:
        cart_nmb += product_in_basket.nmb
    return_dict["cart_nmb"] = cart_nmb
    print(return_dict)
    return JsonResponse(return_dict)

def cart(request):
    session_key = request.session.session_key
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True)
    total_price = 0
    for product_in_basket in products_in_basket:
        total_price += product_in_basket.total_price
    # передаем форму на вьюху
    # form = CartForm(request.POST or None)
    if request.POST:
        print (request.POST)
        if request.POST:
            print ("yes.cart")
            data = request.POST
            for name, value in data.items():
                if name.startswith("product_in_basket_"):
                    products_in_basket_id = name.split("product_in_basket_")[1]
                    product_in_baskets = ProductInBasket.objects.get(
                        session_key=session_key,
                        is_active=True,
                        product__id = products_in_basket_id)
                    product_in_baskets.nmb = value
                    print (value)
                    product_in_baskets.save(force_update=True)



        return HttpResponseRedirect('/checkout/')
    else:
            print ("now")
    return render(request, 'landing/cart.html', locals())

def checkout(request):
    session_key = request.session.session_key
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True).exclude(order__isnull=False)

    total_price = 0
    for product_in_basket in products_in_basket:
        total_price += product_in_basket.total_price
    # передаем форму на вьюху
    form = CheckoutContactForm(request.POST or None)
    if request.POST:

        if form.is_valid():
            print ("yes.checkout")
            print (request.POST)
            data = request.POST
            name = data.get("name", "serg")
            phone = data["phone"]
            mail = data["email"]
            user, created = User.objects.get_or_create(username = name, defaults ={"first_name": name })

            order = Order.objects.create(user = user, customer_name = name,customer_tel = phone, status_id = 1)


            for name, value in data.items():
                if name.startswith("product_in_basket_"):
                    products_in_basket_id = name.split("product_in_basket_")[1]

                    print (products_in_basket_id)


                    product_in_baskets = ProductInBasket.objects.get(session_key=session_key, is_active=True,product__id = products_in_basket_id )

                    product_in_baskets.nmb = value
                    print (product_in_baskets.nmb)
                    print (product_in_baskets)
                    product_in_baskets.save(force_update=True)
                    ProductInOrder.objects.create(
                                                 # id = order,
                                                 product = product_in_baskets.product,
                                                 nmb = product_in_baskets.nmb,
                                                 price_per_item = product_in_baskets.price_per_item,
                                                 total_price = product_in_baskets.total_price,
                                                 order = order

                    )

                    product_in_baskets.delete()

                    send_mail('Интернет магазин всякой х-ни',
                              'Ваш заказ принят,наберитесь терпения и ждите...',
                              'sergsergio777@gmail.com',
                              [mail],
                              )

            return HttpResponseRedirect('/checkout/')
        else:
            print ("now")
    return render(request, 'landing/checkout.html',locals())

def delete_item_in_basket(request,product_id):
    session_key = request.session.session_key
    products_in_baskets = ProductInBasket.objects.get (session_key=session_key, is_active=True,product_id = product_id )
    products_in_baskets.delete()
    # return render(request, 'landing/checkout.html', locals())
    return HttpResponseRedirect('/cart/')

# добавление в карзину с главной страницы
def add_to_cart(request,product_id):
    session_key = request.session.session_key
    product = Product.objects.get( is_active=True,id = product_id)
    nmb = 1
    new_product, created = ProductInBasket.objects.get_or_create(session_key=session_key, product_id=product_id,
                                                                 defaults={"nmb": nmb})
    if not created:
         new_product.nmb += 1
         new_product.save(force_update=True)
    return HttpResponseRedirect('/')

# добавление в карзину с страницы аккаун
def add_to_cart_wishlist(request,product_id):
    session_key = request.session.session_key
    product = Product.objects.get( is_active=True,id = product_id)
    nmb = 1
    new_product, created = ProductInBasket.objects.get_or_create(session_key=session_key, product_id=product_id,
                                                                 defaults={"nmb": nmb})
    if not created:
         new_product.nmb += 1
         new_product.save(force_update=True)
    return HttpResponseRedirect('/cart/')