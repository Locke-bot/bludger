from django import forms
from django.db import models
from .models import UserComment

class CommentForm(forms.ModelForm):
    class Meta:
        model = UserComment
        fields = '__all__'
    
