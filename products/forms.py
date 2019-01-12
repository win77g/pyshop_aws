from django import forms
from .models import *

from .models import Product



class SearchForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name']