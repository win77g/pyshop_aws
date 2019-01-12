from django.contrib import admin
from .models import *

class SubAdmin (admin.ModelAdmin):
    # list_display = ["name","email"]
    #  вывод всех полей в админку
      list_display = [field.name for field in Subscribes._meta.fields]
    #  фильтр  натройка
      list_filter = ['name','email']
    #   поиск
      search_fields = ['id','name','email','tel']

class Meta:
    model = Subscribes
# Register your models here.
admin.site.register(Subscribes,SubAdmin)