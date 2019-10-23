'''
Created on May 6, 2019

@author: Deep
'''
from django.shortcuts import render

def welcomePage(request):
    return  render (request,"./index.html")