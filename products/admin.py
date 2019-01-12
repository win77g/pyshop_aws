from django.contrib import admin
from .models import *

class CategoryAdmin (admin.ModelAdmin):
   #  вывод всех полей в админку
      list_display = [field.name for field in Category._meta.fields]

      class Meta:
           model = Category
# Register your models here.
admin.site.register(Category, CategoryAdmin)


class ProductCategoryAdmin (admin.ModelAdmin):
   #  вывод всех полей в админку
      list_display = [field.name for field in ProductCategory._meta.fields]

      class Meta:
           model = ProductCategory
# Register your models here.
admin.site.register(ProductCategory, ProductCategoryAdmin)

# class ProductSubCategoryAdmin (admin.ModelAdmin):
#    #  вывод всех полей в админку
#       list_display = [field.name for field in ProductSubCategory._meta.fields]
#
#       class Meta:
#            model = ProductSubCategory
# # Register your models here.
# admin.site.register(ProductSubCategory, ProductSubCategoryAdmin)



#добавление фоток внизу прдукт админки
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0


# Register your models here.
class ProductAdmin (admin.ModelAdmin):
   #  вывод всех полей в админку
   #    list_display = [field.name for field in Product._meta.fields]
   #    inlines = [ProductImageInline]
   list_display = ['name','image_img', 'price', 'price_old','categ','is_active','new_product','top','created','updated']
   readonly_fields = ['image_img',]
   # fields = ['category', 'title', 'slug', 'metakey', 'metadesc', 'text_redactor', 'text_redactor_full', 'tag', 'timestamp', 'autor', 'image', 'image_img', 'body', 'likes', 'dislikes']

class Meta:
    model = Product
# Register your models here.
admin.site.register(Product,ProductAdmin)



# Register your models here.
class ProductImageAdmin (admin.ModelAdmin):
   #  вывод всех полей в админку
      list_display = [field.name for field in ProductImage._meta.fields]

class Meta:
    model = ProductImage
# Register your models here.
admin.site.register(ProductImage,ProductImageAdmin)
