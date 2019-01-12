from django import forms
from .models import *

class CheckoutContactForm(forms.Form):
    name = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    email = forms.CharField(widget=forms.EmailInput({'placeholder': 'example@mail.ru', 'autocomplete': 'on'})
                            , max_length=30, )
class CartForm(forms.Form):
    # name = forms.CharField(required=True)
    # phone = forms.CharField(required=True)
    nmb = forms.CharField(required=True)
