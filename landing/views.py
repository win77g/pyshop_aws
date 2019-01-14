from django.shortcuts import render,render_to_response,redirect
from .forms import SubscriberForm
from .forms import RegistrationForm,LoginForm
from products.models import ProductImage
from products.models import *
from orders.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.edit import FormView
from django.contrib.auth import logout,login,authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
#для регистрации и активации пользователя
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import send_mail
# Create your views here.

def landing(request):

   form = SubscriberForm(request.POST or None)

   if request.method== "POST" and form.is_valid():
      print(request.POST)
      print(form.cleaned_data)
      new_form = form.save()

   return render(request, 'landing/landing.html',locals())

def home(request):
   products = Product.objects.filter(is_active=True,categ__id = 2,top = True   )
   # products_images_electro = products_images.filter(categ__id = 1,top = True,)
   category = Category.objects.all()

   return render(request, 'landing/home.html',locals())

def register(request):
   form = RegistrationForm(request.POST or None)
   if form.is_valid():
       # form.save(commit=False)
       user = form.save(commit=False)
       # Cleaned(normalized) data
       username = form.cleaned_data['username']
       password = form.cleaned_data['password']
       mail = form.cleaned_data['email']
       #передаем переменные в функцию activate

       #  Use set_password here
       user.set_password(password)
       user.is_active = False
       user.save()
       #подтверждение регистрации
       current_site = get_current_site(request)
       message = render_to_string('acc_active_email.html', {
           'user': user,
           'domain': current_site.domain,
           'uid': urlsafe_base64_encode(force_bytes(user.pk)),
           'token': account_activation_token.make_token(user),
           'password':password
       })
       send_mail('Интернет магазин всякой х-ни',
                 message
                 ,
                 'sergsergio777@gmail.com',
                 [mail],
                 )

       return HttpResponseRedirect('/login_two/')
   context = {'form' : form}
   return render(request, 'landing/register.html', context)


#функция активации пользователя
def activate(request, uidb64, token, ):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        # login(request, user)
        # return redirect('home')
        return HttpResponseRedirect('/login/')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        # return render(request, 'login.html', {'form': form})
    else:
        return HttpResponse('Activation link is invalid!')

# def login(request):
#     return render(request, 'login.html')

def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        login_user = authenticate(username=username,
                                  password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('home'))
    return render(request, 'landing/login.html', locals())

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

# метод просмотра  кабинета
def account(request):
   order = Order.objects.filter(customer_name = request.user )
   product = ProductInOrder.objects.filter(order__customer_name=request.user)
   wishlist = Wishlist.objects.filter(user = request.user)
   return render(request, 'landing/account.html', locals())

# метод просмотра заказа из кабинета
def order(request):
    data = request.POST
    order_id = data.get("order_id")
    product = ProductInOrder.objects.filter(order=order_id)
    # for att in dir(product):
    #         print (att, getattr(product, att))

    return render(request, 'modal_order.html', locals())
# вывод товара в модальное окно
def productview(request):
    data = request.POST
    product_id = data.get("product_id")
    product = Product.objects.filter(is_active=True,id=product_id)
    # for att in dir(product):
    #         print (att, getattr(product, att))

    return render(request, 'modal_view_product.html', locals())

# вывод товара в модальное окно wishlist
def wishlist(request):
    data = request.POST
    product_id = data.get("product_id")
    product = Product.objects.filter(is_active=True,id=product_id)
    product_wish = Product.objects.get(id=product_id)
    user = request.user
    get_wishlest = Wishlist.objects.filter(user=user,product=product_wish)
    if not get_wishlest:
        wishlist = Wishlist.objects.create(user=user,product=product_wish)
    # for att in dir(product_wish):
    #         print (att, getattr(product_wish, att))
    return render(request, 'wishlist_modal.html', locals())

def delete_item_in_wishlist(request,product_id):
    # print (product_id)
    product = Product.objects.filter(id = product_id)
    products_in_wishlist = Wishlist.objects.get (user = request.user,product = product )
    products_in_wishlist.delete()
    # return render(request, 'landing/checkout.html', locals())
    return HttpResponseRedirect('/account/')

def register_alarm():
    return HttpResponseRedirect('/account/')

