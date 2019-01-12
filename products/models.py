from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor_uploader.fields import RichTextUploadingField
# import mptt



class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children',verbose_name="Родитель", db_index=True)
    slug = models.SlugField(verbose_name='Транслит', null = True)

    def __str__(self):
        return " %s" % self.name

    class MPTTMeta:
        order_insertion_by = ['name']


# модель категории
class ProductCategory(models.Model):
    name_category = models.CharField(max_length=120, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return " %s" % self.name_category
    class Meta:
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категория товаров'

# модель субкатегории
# class ProductSubCategory(models.Model):
#     name_subcategory = models.CharField(max_length=120, blank=True, null=True, default=None)
#     category = models.ForeignKey(ProductCategory, blank=True, null=True, default=None)
#     is_active = models.BooleanField(default=True)
#
#     def __str__(self):
#         return " %s" % self.name_subcategory
#     class Meta:
#         verbose_name = 'Подкатегория товара'
#         verbose_name_plural = 'Подкатегория товаров'_

def image_folder(instance,filename):
    filename = instance.slug +'.'+filename.split('.')[1]
    return "{0}/{1}".format(instance.slug,filename)

class Product(models.Model):
    name = models.CharField(max_length=120,blank=True, null=True, default=None)
    image = models.ImageField(upload_to=image_folder, blank=True, null=True, default=None)
    slug = models.SlugField(blank=True, null=True, default=None)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_old = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = RichTextUploadingField(config_name='default')
    description_short = RichTextUploadingField(config_name='default')
    discount = models.IntegerField(default=0)
    # category = models.ForeignKey(ProductCategory,blank=True, null=True, default=None )
    categ = TreeForeignKey(Category, blank=True, null=True,related_name = 'cat')
    is_active = models.BooleanField(default=True)
    new_product = models.BooleanField(default=False)
    top = models.BooleanField(default=False)
    comments = models.TextField(blank=True, null=True, default=None)
    created = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated = models.DateTimeField(auto_now_add=False,auto_now=True)



    # вывод одного поля
    def __str__(self):
        return " %s" % self.name
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def image_img(self):
        if self.image:
            return u'<a href="{0}" target="_blank"><img src="{0}" width="100"/></a>'.format(self.image.url)
        else:
            return '(Нет изображения)'
    image_img.short_description = 'Картинка'
    image_img.allow_tags = True

# фотки продукта
class ProductImage(models.Model):
    product = models.ForeignKey(Product,blank=True, null=True, default=None)
    image = models.ImageField(upload_to='product_images/')
    is_main = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated = models.DateTimeField(auto_now_add=False,auto_now=True)

    # вывод одного поля
    # def __str__(self):
    #     return self.id
    # class Meta:
    #     verbose_name = 'Фотография'
    #     verbose_name_plural = 'Фотографии'
