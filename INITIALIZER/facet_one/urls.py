# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 19:36:20 2020

@author: Zen
"""

from django.urls import path, reverse
from django.views.generic import TemplateView
from django.conf.urls import url
import facet_one.views as one_views

app_name = 'facet_one'

urlpatterns = [
    url(r'^thankyou/(?P<name>\w+)', TemplateView.as_view(template_name='thankyou.html'), name='thankyou'),
    url(r'^(?P<page_id>\d+)?', one_views.AboutPageView, name='about_page'),
]
