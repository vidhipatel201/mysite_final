'''
Created on Jun 9, 2019

@author: Deep
'''
from django import forms
from myapp.models import Order,Client, Product
from django.contrib.gis.db.backends.spatialite import client
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client', 'product', 'num_units']
        
    client = forms.ModelChoiceField(queryset = Client.objects.all(), label = 'Client Name')
    product = forms.ModelChoiceField(queryset= Product.objects.all())
    num_units = forms.IntegerField(label='Quantity')
    
class InterestForm(forms.Form):
    CHOICES = [('1', 'Yes'), ('2', 'No')]
    interested = forms.ChoiceField(widget = forms.RadioSelect, choices = CHOICES)
    quantity = forms.IntegerField(min_value=1, initial =1)
    comments = forms.CharField(label = 'Additional Comments', widget = forms.Textarea)

class ClientForm(UserCreationForm):
    class Meta:
        model = Client
        fields = ['username', 'first_name', 'last_name', 'email','password1','password2']
    
    first_name = forms.CharField(label = 'First Name', max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(label = 'Last Name', max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(label = 'Email', max_length=254, help_text='Required. Inform a valid email address.')
    