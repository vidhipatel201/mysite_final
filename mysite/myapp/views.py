from django.shortcuts import get_object_or_404, render, redirect
from .models import Category, Product, Client, Order
from .forms import OrderForm, InterestForm, ClientForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.generic.base import View

# Create your views here.


def index(request):
    if 'last_login' in request.session:
        last_log = request.session.get('last_login')
    else:
        last_log = "Your last login was more than one hour ago"
    cat_list = Category.objects.all().order_by('id')[:10]
    prod_list = Product.objects.all().order_by('-price')[:5]
    return render(request, 'myapp/index.html', {'cat_list': cat_list, 'expProd':prod_list, 'last_log':last_log})


def about(request):
    if request.session.has_key('username'):
        cookieValue = request.COOKIES.get('no_of_visit', 'default') 
        if cookieValue == 'default':
            response = render(request, 'myapp/about.html', {'no_of_visit': '1'})
            response.set_cookie('no_of_visit', 1, 5 * 60)
            return response
        else:
            cookieValue = int(cookieValue) + 1
            response = render(request, 'myapp/about.html', {'no_of_visit': cookieValue})
            response.set_cookie('no_of_visit', cookieValue)
            return response
    else:
        return redirect('/myapp/login')


class IndexView(View):

    def get(self, request):
        if 'last_login' in request.session:
            last_log = request.session.get('last_login')
        else:
            last_log = "Your last login was more than one hour ago"
        cat_list = Category.objects.all().order_by('id')[:10]
        prod_list = Product.objects.all().order_by('-price')[:5]
        return render(request, 'myapp/index.html', {'cat_list': cat_list, 'expProd':prod_list, 'last_log':last_log})


class AboutView(View):

    def get(self, request):
        if request.session.has_key('username'):
            cookieValue = request.COOKIES.get('no_of_visit', 'default') 
            if cookieValue == 'default':
                response = render(request, 'myapp/about.html', {'no_of_visit': '1'})
                response.set_cookie('no_of_visit', 1, 5 * 60)
                return response
            else:
                cookieValue = int(cookieValue) + 1
                response = render(request, 'myapp/about.html', {'no_of_visit': cookieValue})
                response.set_cookie('no_of_visit', cookieValue)
                return response
        else:
            return redirect('/myapp/login')

    
def detail(request, cat_no):
    cat = get_object_or_404(Category, pk=cat_no)
    products = Product.objects.filter(category__pk=cat_no)
    return render(request, 'myapp/detail.html', {'cat': cat, 'prod_list':products})


def products(request):
    prodlist = Product.objects.all().order_by('id')[:10]
    return render(request, 'myapp/products.html', {'prodlist': prodlist})        


def productdetail(request, prod_id):
    product = Product.objects.get(pk=prod_id)
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            data = form.data
            if data.get('interested') == '1':
                print('ProductInt', product.interested)
                product.interested = product.interested + 1
            product.save()
            print('AfterProductInt', product.interested)
        return redirect('myapp:index')
    else:
        form = InterestForm()
    return render(request, 'myapp/productdetails.html', {'form':form, 'prod':product})

    
def place_order(request):
    msg = ''
    prodlist = Product.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.num_units <= order.product.stock:
                prod = order.product
                prod.stock -= order.num_units 
                prod.save()
                order.save()
                
                msg = 'Your order has been placed successfully.'
            else:
                msg = 'We do not have sufficient stock to fill your order.'
            return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = OrderForm()
    return render(request, 'myapp/placeorder.html', {'form':form, 'msg':msg, 'prodlist':prodlist})


def user_login(request):
    if request.method == 'POST':
        usern = request.POST['username']
        passw = request.POST['password']
        user = authenticate(username=usern, password=passw)
        if user:
            if user.is_active:
                login(request, user)
                current_login_time = str(datetime.datetime.now())
                request.session['last_login'] = current_login_time
                request.session.set_expiry(60 * 60)
                request.session['username'] = usern
                return HttpResponseRedirect(reverse('myapp:my_order'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')


def register_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            msg = 'Successfully registered! Kindly log in'
            return render(request, 'myapp/register.html', {'msg':msg})
        else:
            return render(request, 'myapp/register.html', {'form':ClientForm()})
    else:
        form = ClientForm()
        return render(request, 'myapp/register.html', {'form':form})    


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('myapp:user_login')))


@login_required
def myorders(request):
    order = Order.objects.filter(client__username=request.user.username)
    return render(request, 'myapp/myorder.html', {'order': order})
