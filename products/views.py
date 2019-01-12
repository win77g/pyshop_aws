from django.shortcuts import render

from products.models import *
from products.models import ProductCategory
from .forms import SearchForm
from django.db.models import Q
from django.core.paginator import Paginator
# Create your views here.

def product (request,product_id):
    product = Product.objects.get(id=product_id)
    # category_main = ProductCategory.objects.all()

    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()
    print (request.session.session_key)
    return render(request, 'products/products.html', locals())
# получение страницы с товарами по id категории
def category(request,id ):
    categorys = Category.objects.filter(id = id)
    categ = Category.objects.filter(parent = categorys)
    # for att in dir(categ):
    #  print (att, getattr(categorys, att))

    # products_images = ProductImage.objects.filter(is_active=True, product__categ=categorys)
    # для heroku
    products_images = Product.objects.filter(is_active=True, categ=categorys)

    page = request.GET.get('page',1)
    paginator = Paginator(products_images, 3)  # Show 25 contacts per page

    try:
        product_page = paginator.page(page)
    except PageNotAnInteger:
        product_page = paginator.page(1)
    except EmptyPage:
        product_page = paginator.page(paginator.num_pages)

    return render(request, 'products/category.html', locals())

def search(request):
    # form = SearchForm(request.POST or None)
    # args = {}
    # args['product'] = Product.objects.all()
    # args['form_search'] = search_form
    if request.POST:
        key = request.POST.get('q')
        founded_product = Product.objects.filter(
            Q(name__icontains = key) |
            Q(description__icontains = key) |
            Q(description_short__icontains = key))
        args = {'founded_product':founded_product}
        print (founded_product)

    return render(request, 'products/search.html', locals())


