# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 21:54:20 2020

@author: Zen
"""
from django.core.management.base import CommandError, BaseCommand
from django.conf import settings
import sys

class Command(BaseCommand):
    help = "outline shit"
    
    def handle(self, *args, **kwargs):
        try:
            sys.stdout.write(self.style.SUCCESS('\n'.join(settings.INSTALLED_APPS)))
        except Exception as e:
            sys.stderr.write(self.style.WARNING('Shit Happened'))
