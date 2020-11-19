# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 23:12:59 2020

@author: Zen
"""

from django import forms
from .models import Blog
import json

class SignInForm(forms.Form):
    Identifier = forms.CharField(label='Username/Email')
    Password = forms.CharField(widget=forms.PasswordInput())
    
# class ContactForm(forms.Form):
#     username = forms.CharField(max_length=20)
#     password = forms.CharField(widget=forms.PasswordInput())
#     email = forms.EmailField(label='Your Email')
#     choices = []
#     with open(r'C:\Users\ZAINAB\Desktop\Library\country-by-capital-city.json', 'r') as fh:
#         xc = json.loads(fh.read()) 
#         for country_capital in xc:
#             country = country_capital['country'] 
#             choices.append((country, country)) 
#     choices = tuple(choices) 
#     country = forms.ChoiceField(label='choices', choices=(choices)) 
#     remember = forms.BooleanField(label='Remember me', required=False) 
    
#     def clean_username(self):
#         value = self.cleaned_data['username']
#         if not len(value) >= 1: # ty is a name, I think not that i give a shit or somethin'
#              self.add_error('userame', 'Username too short.')
#         return value
    
#     def clean_email(self):
#         value  = self.cleaned_data['email']
#         if Persons.objects.filter(username=self.cleaned_data['username']).exists(): # username already esists
#             return value
#         if Persons.objects.filter(email=value).exists(): # email already in use
#             self.add_error('email', 'email already connected to another user')
#         return value
    
#     def clean_username(self):
#         value = self.cleaned_data['username']
#         if Persons.objects.filter(username=value).exists(): # username already esists
#             self.add_error('username', 'username already exists')
#         return value
    
#     def clean_password(self):
#         value = self.cleaned_data['password']
#         if not len(value) >= 5:
#             self.add_error('password', 'password must be at least five characters')
#         if not any([str(i) in value for i in range(0, 10)]):
#             self.add_error('password', 'password must contain at least one digit')
#         return value
            