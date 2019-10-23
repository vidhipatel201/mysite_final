from django.urls import path
from myapp import views
from django.contrib.auth.forms import UserCreationForm
from myapp.models import Client
from django.views.generic.edit import CreateView
from django.urls import reverse
from myapp.views import IndexView, AboutView
from django.urls.conf import include

app_name = 'myapp'

urlpatterns = [
#  path(r'', views.index, name='index'),
 path(r'', IndexView.as_view(), name='index'),
 path(r'about/', AboutView.as_view(), name='about'),
 path(r'products/', views.products, name='products'),
 path(r'<int:cat_no>/', views.detail, name='detail'),
 path(r'place_order/', views.place_order, name='place_order'),
 path(r'products/<int:prod_id>/', views.productdetail, name='productdetail'),
 path(r'login/', views.user_login, name='user_login'),
 path(r'myorder/', views.myorders, name='my_order'),
 path(r'logout/', views.user_logout, name='logout'),
 path(r'register/', views.register_client, name='register_client'),
 #path(r'register/', (CreateView.as_view(model=Client, get_success_url =lambda: reverse('create_user'), form_class=UserCreationForm, template_name="myapp/register.html")), name='create_user'),
 ]