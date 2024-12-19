from asgiref.sync import sync_to_async
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django import forms
from .models import *


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Обязательное поле. Введите действующий email.')
    phone_number = forms.CharField(max_length=15, required=False, help_text='Необязательное поле.')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class TypeForm(forms.Form):
    name = forms.CharField(max_length=25)


def choice():
    types = ()
    for i in Type.objects.all():
        types = types + ((i,i),)
    return types


class ProductForm(forms.Form):
    name = forms.CharField(max_length=50)
    prise = forms.FloatField()
    img_url = forms.CharField(widget=forms.URLInput())
    type = forms.ChoiceField(choices=choice())
    count = forms.IntegerField(min_value=0, step_size=1)
    cost_price = forms.FloatField()
class FeedbackForm(forms.Form):
    question = forms.CharField(max_length=25, label='Тема обращения/вопрос')
    description = forms.CharField(max_length=500, label='Описание проблемы', widget=forms.Textarea())