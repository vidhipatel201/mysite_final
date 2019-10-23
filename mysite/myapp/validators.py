'''
Created on Jun 27, 2019

@author: Deep
'''
from django.core.exceptions import ValidationError

def validate_product_stock(value):
    if not value < 0 and value>1000:
        raise ValidationError("Please enter values between 0 and 1000")
    else:
        return value
