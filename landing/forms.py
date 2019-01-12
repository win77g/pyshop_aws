import os
import gzip

from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.utils._os import upath
from pathlib import Path
from django.core.mail import send_mail
# from django.contrib.auth.forms import AuthenticationForm




class SubscriberForm(forms.ModelForm):

    class Meta:
        model = Subscribes
        exclude = [""]

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'


    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        # password_check = self.cleaned_data['password_check']

        if not User.objects.filter(username = username).exists():
            raise forms.ValidationError('Такой логин не зарегистрирован!')
        user = User.objects.get(username=username)
        print(user)
        print(password)
        if user and not user.check_password(password):
            raise forms.ValidationError('Вы ввели не верный пароль!')


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput,min_length = 8,max_length = 15)
    password_check = forms.CharField(widget=forms.PasswordInput)
    email = forms.CharField(widget=forms.EmailInput({'placeholder':'example@mail.ru','autocomplete':'on'})
                                                    ,max_length = 30,)
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'password_check',
            ]

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['password'].help_text = 'Придумайте пароль.Не более 15 символов.'
        self.fields['password_check'].label = 'Пароль'
        self.fields['first_name'].label = 'Фамилия'
        self.fields['last_name'].label = 'Имя'
        self.fields['email'].label = 'Ваша почта'
        self.fields['email'].help_text = 'Пример (example@mail.ru).Не более 30 символов.'

    # проверяем на совподение полей в системе
    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']
        email = self.cleaned_data['email']
        if User.objects.filter(username = username).exists():
            raise forms.ValidationError({'username':'Пользователь с логином '  +username+  ' уже зарегистрирован в системе!'},
                                        code='user exists')
        if User.objects.filter(email = email).exists():
            raise forms.ValidationError({'email':'Пользователь с email '  +email+  ' уже зарегистрирован!'}, code='email exists')
        if password != password_check:
            raise forms.ValidationError({
                                         'password': '',
                                         'password_check': 'Вы ошиблись при вводе паролей, они не совпадают, введите повторно!'},
                code='passwords do not match',)
        # send_mail('Интернет магазин всякой х-ни',
        #           'Поздравлям вас ,вы успешно зарегистрировались в интернет магазине '+'Ваш пароль:'+password
        #           + ' Ваш логин:' + username
        #           ,
        #           'sergsergio777@gmail.com',
        #           [email],
        #           )
    # Подключаем валидацию от джанго
    def clean_password(self):
        password = self.cleaned_data.get('password')
        try:
            password_validation.validate_password(password, self.instance)
        except forms.ValidationError as error:

            # Method inherited from BaseForm
            self.add_error('password', error)
        return password









