from itertools import product
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.utils.timezone import localdate

from .form import *
from .models import *
import json
from urllib.parse import unquote
from django.contrib.sessions.models import Session
from django.contrib.auth.views import *


def redirect_to_home(request):
    return redirect('home')


def n_days_ago(data, n):
    mouth = {
        1: 31,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31
    }
    dats = data.split('-')
    dats[0] = int(dats[0])
    dats[1] = int(dats[1])
    dats[2] = int(dats[2])
    for i in range(n):
        if dats[2] != 1:
            dats[2] -= 1
        else:
            if dats[1] != 1:
                dats[1] -= 1
                if dats[1] != 2:
                    dats[2] = mouth[dats[1]]
                else:
                    if dats[0] % 4 == 0 and (dats[0] % 100 != 0 and dats[0] % 400 != 0):
                        dats[2] = 29
                    else:
                        dats[2] = 28
            else:
                dats[0] -= 1
                dats[1] = 12
                dats[2] = mouth[dats[1]]
    return f"{dats[0]}-{'0' * (2 - len(str(dats[1])))}{dats[1]}-{'0' * (2 - len(str(dats[2])))}{dats[2]}"


def most_by_product():
    today = localdate()
    one_week_before = n_days_ago(str(today), 7)
    sells = Sell.objects.filter(date__range=[one_week_before, today])
    res = {}
    for i in sells:
        if i.product in res.keys():
            res[i.product] += i.count
        else:
            res[i.product] = i.count
    max_value = 0
    product_obj = ''
    for i in res:
        if res[i] > max_value:
            max_value = res[i]
            product_obj = i
    return product_obj


def get_user_from_session(session_key):
    try:
        session = Session.objects.get(session_key=session_key)
        uid = session.get_decoded().get('_auth_user_id')
        return CustomUser.objects.get(pk=uid)
    except:
        return None


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/reg.html', {'form': form})


def login_view(request):
    form = LoginForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                response = redirect('home')
                return response
    return render(request, 'registration/log.html', {'form': form})


def home_view(request):
    most = most_by_product()
    types = Type.objects.all()
    name = request.GET.get('name', '')
    type_id = request.GET.get('type', '')
    products = Product.objects.all()
    if name != '' and type_id != '':
        type = Type.objects.get(id=type_id)
        products = Product.objects.all().filter(name=name, type=type)
    elif name != '':
        products = Product.objects.all().filter(name=name)
    elif type_id != '':
        type = Type.objects.get(id=type_id)
        products = Product.objects.all().filter(type=type)

    return render(request, 'home/homepage.html', {'products': products, 'most': most, "types": types, "name": name})


def log_out(request):
    response = redirect('login')
    response.delete_cookie('sessionid')
    return response


@login_required(login_url='login')
def site_admin(request):
    form_type = TypeForm()
    form_product = ProductForm()
    orders = Order.objects.all()
    if request.method == 'POST':
        request.POST.get('')
    return render(request, 'admin/admin.html', {'orders': orders, 'form_product': form_product})


@login_required(login_url='login')
def create_type(request):
    form_type = TypeForm()
    if request.method == 'POST':
        name = request.POST.get('name')
        product_type = Type(name=name)
        print(name)

        product_type.save()
        return redirect('admin')
    return render(request, 'admin/admin_type.html', {'form_type': form_type})


@login_required(login_url='login')
def create_product(request):
    form_product = ProductForm()
    if request.method == 'POST':
        name = request.POST.get('name')
        prise = request.POST.get('prise')
        img_url = request.POST.get('img_url')
        product_type = request.POST.get('type')
        product_count = request.POST.get('count')
        cost_price = request.POST.get('cost_price')
        product_type = Type.objects.get(name=product_type)
        product = Product(name=name, prise=prise, img_url=img_url, type=product_type, count=product_count,
                          cost_price=cost_price)
        product.save()

        return redirect('admin')
    return render(request, 'admin/admin_product.html', {'form_product': form_product})


@login_required(login_url='login')
def buy_product(request, product_id):
    sessionid = request.COOKIES.get('sessionid')
    user = get_user_from_session(sessionid)
    product = Product.objects.get(id=product_id)
    if product.count == 0:
        return redirect(info_product, product.id)
    user.cart.add(product)
    user.save()
    print(product)
    return redirect('home')


@login_required(login_url='login')
def delete_product_from_order(request, id):
    sessionid = request.COOKIES.get('sessionid')
    user = get_user_from_session(sessionid)
    user.cart.remove(id)
    user.save()
    return redirect('profile')


@login_required(login_url='login')
def profile_view(request):
    sessionid = request.COOKIES.get('sessionid')
    user = get_user_from_session(sessionid)
    if request.method == 'POST':
        if len(user.cart.all()) > 0:
            order = Order(user=user)
            order.save()
            user_cart = user.cart.all()
            for i in user_cart:
                cart_count = request.POST.get(str(i.id))
                if int(cart_count) > 0:
                    count = CountProduct(product=i, count=cart_count)
                    count.save()
                    order.count.add(count)
                    sell_list = AdminSellList.objects.get(product=i)
                    sell_list_count = int(sell_list.count)
                    sell_list.count = str(sell_list_count + int(cart_count))
                    i.count -= int(cart_count)
                    sell = Sell(product=i, count=cart_count, date='2024-11-17')
                    sell.save()
                    i.save()

                    sell_list.save()
            order.save()
            if len(order.count.all()) == 0:
                order.delete()
            user.cart.clear()
    return render(request, 'profile/profile.html', )


@login_required(login_url='login')
def complete_order(request, id):
    sessionid = request.COOKIES.get('sessionid')
    user = get_user_from_session(sessionid)
    if user.is_staff:
        order = Order.objects.get(id=id)
        order.delete()
    return redirect('admin')


@login_required(login_url='login')
def info_product(request, product_id):
    sessionid = request.COOKIES.get('sessionid')
    user = get_user_from_session(sessionid)
    product = Product.objects.get(id=product_id)
    admin_list = AdminSellList.objects.get(product=product)
    admin_list.flyers += 1
    print(admin_list.flyers)
    admin_list.save()
    if request.method == "POST":
        evaluation = int(request.POST.get('evaluation'))
        text = request.POST.get('text')
        product.count_evaluation += 1
        if product.numm_evaluation == 0:
            product.numm_evaluation = evaluation
        else:
            product.numm_evaluation = (product.numm_evaluation + evaluation) / 2
        product.save()
        class_evaluation = Evaluation(product=product, user=user, text=text, evaluation=evaluation)
        class_evaluation.save()
    evaluations = Evaluation.objects.all()
    return render(request, 'home/product_info.html', {'product': product, "evaluations": evaluations})


@login_required(login_url='login')
def change_product(request, id):
    product = Product.objects.get(id=id)
    types = Type.objects.all()
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.prise = request.POST.get('prise')
        product.img_url = request.POST.get('img_url')
        product_type = Type.objects.get(id=request.POST.get('type'))
        product.type = product_type
        product.count = request.POST.get('count')
        product.cost_price = request.POST.get('cost_price')
        product.save()
        return redirect('info_product', id)
    product.prise = str(product.prise).replace(',', '.')
    product.cost_price = str(product.cost_price).replace(',', '.')
    return render(request, 'admin/change_product.html', {'types': types, 'product': product})


@login_required(login_url='login')
def change_info(request):
    # for i in Product.objects.all():
    #     i.delete()
    sessionid = request.COOKIES.get('sessionid')
    user = get_user_from_session(sessionid)
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.phone_number = request.POST.get('phone_number')
        user.save()
        return redirect('profile')
    return render(request, 'profile/change_info.html')


@login_required(login_url='login')
def feedback_views(request):
    sessionid = request.COOKIES.get('sessionid')
    user = get_user_from_session(sessionid)
    form = FeedbackForm()
    if request.method == 'POST':
        question = request.POST.get('question')
        description = request.POST.get('description')
        feedback = Feedback(question=question, description=description, user=user)
        feedback.save()
        return redirect('home')
    return render(request, 'home/feedback.html', {'form': form})


@login_required(login_url='login')
def feedback_list(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'admin/feedback_list.html', {'feedbacks': feedbacks})


@login_required(login_url='login')
def feedback_completed(request, id):
    sessionid = request.COOKIES.get('sessionid')
    user = get_user_from_session(sessionid)
    if user.is_staff:
        feedback = Feedback.objects.get(id=id)
        feedback.delete()
    return redirect('feedback_list')


@login_required(login_url='login')
def statistics(request):
    sessionid = request.COOKIES.get('sessionid')
    user = get_user_from_session(sessionid)
    if user.is_staff:
        AdminSellLists = AdminSellList.objects.all().order_by('count')
        AdminSellLists = AdminSellLists[::-1]
        return render(request, 'admin/admin_statistics.html', {'AdminSellLists': AdminSellLists})
    return redirect('home')


@login_required(login_url='login')
def detail_statistics(request):
    sessionid = request.COOKIES.get('sessionid')
    user = get_user_from_session(sessionid)
    if user.is_staff:
        start = request.GET.get('start', None)
        finish = request.GET.get('finish', None)
        sells = Sell.objects.all()
        if finish == '' or finish is None:
            finish = localdate()
        if start == '' or start is None:
            start = '0001-01-01'

        sells = Sell.objects.filter(date__range=[start, finish])
        today = localdate()
        # filter(date__range=[n_days_ago(str(today),7), today])
        return render(request, 'admin/admin_statistics_detailed.html', {'sells': sells, 'now': today})
    return redirect('home')


@login_required(login_url='login')
def feedback_answer(request, id):
    sessionid = request.COOKIES.get('sessionid')
    user = get_user_from_session(sessionid)
    feedback = Feedback.objects.get(id=id)
    if user.is_staff:
        if request.method == "POST":
            email = feedback.user.email
            title = request.POST.get('title')
            text = request.POST.get('text')
            send_mail(title, text, settings.EMAIL_HOST_USER, [email])
            feedback.delete()
            return redirect('feedback_list')
        return render(request, 'admin/feedback_answer.html')
    return redirect('home')


@login_required(login_url='login')
def delete_product(request, id):
    sessionid = request.COOKIES.get('sessionid')
    user = get_user_from_session(sessionid)
    product = Product.objects.get(id=id)
    if user.is_staff:
        product.delete()
    return redirect('home')


@login_required(login_url='login')
def analitic(request, id):
    sessionid = request.COOKIES.get('sessionid')
    user = get_user_from_session(sessionid)
    product = Product.objects.get(id=id)
    list_sell = AdminSellList.objects.get(product=product)
    sells = Sell.objects.all().filter(product=product)
    count_sells = len(sells)
    of_by = str(count_sells / list_sell.flyers * 100) + '%'
    money = list_sell.count * (list_sell.product.prise - list_sell.product.cost_price)
    if user.is_staff:
        return render(request, 'admin/analitic.html', {'list_sell': list_sell, 'of_by': of_by, "money": money})
    return redirect('home')


@login_required(login_url='login')
def analitic_list(request):
    sessionid = request.COOKIES.get('sessionid')
    user = get_user_from_session(sessionid)
    products = Product.objects.all()
    if user.is_staff:
        return render(request, 'admin/analitic_list.html', {'products': products})
    return redirect('home')
