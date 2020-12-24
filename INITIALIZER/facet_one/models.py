from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms
from django.forms import formset_factory
from django.utils.html import mark_safe
from django.urls import reverse
from django.contrib.auth.models import User
import datetime

class LiveBlog(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=self.model.LIVE_STATUS)
        
class DraftBlog(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=self.model.DRAFT_STATUS) 
        
class UrlCount(models.Model):
    id = models.AutoField(primary_key=True)
    count = models.PositiveIntegerField(default=0)
    date = models.DateField()
    Url = models.CharField(max_length=500)
    description = models.CharField(max_length=50, help_text="link descriptor (homepage, e.t.c)")
    
    def __str__(self):
        return f"{self.date.strftime('%b %d %Y')} {self.description} {self.count}" # note the url is lower cased, it's accessing the Url Modle below
    

class Url(models.Model): 
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=500, unique=True) # won't use URL field 'cause I will be dealing in relative urls
    descriptor = models.CharField(max_length=50, help_text="link descriptor (homepage, e.t.c)")
    date_added = models.DateField(auto_now_add=True) # date link added
    url_visit_count = models.OneToOneField(UrlCount, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.descriptor 
    
class LinksVisit(models.Model): 
    id = models.AutoField(primary_key=True)
    today_date = models.DateField(unique=True)  # visits on a daily stats
    no_of_visits = models.PositiveIntegerField(default=0) # total number of links visited daily.
    #relation between each url and the no of times visited 
    
    def __str__(self): 
        return f"{self.today_date} {self.no_of_visits}"
    
class StaffManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_staff=True)
    
class Staff(User):
    
    StaffManager = StaffManager()
    
    class Meta:
        proxy = True
    
class Blog(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Staff, on_delete=models.PROTECT)  # deciding 2 authors can't be credited witha asingle post.
    datetime_added = models.DateTimeField(auto_now_add=True, verbose_name='date&time added') 
    last_updated = models.DateTimeField(auto_now=True, blank=True)
    title = models.CharField(max_length=50, unique=True)
    blog_image = models.ImageField(upload_to="blog_images", null=True, help_text="the image associated with the blog")
    blog_image_description = models.CharField(blank=True, null=True, max_length=200, help_text="serves as the alt attribute of the image tag")
    body = models.TextField() 
    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    STATUS_CHOICES = (
            (LIVE_STATUS, 'Live'),
            (DRAFT_STATUS, 'Draft'),
        )
    status = models.IntegerField(choices=STATUS_CHOICES) 
    COMMENT_ENABLE = 1
    COMMENT_DISABLED = 2
    ENABLECOMMENT_CHOICES = (
            (COMMENT_ENABLE, 'enable'),
            (COMMENT_DISABLED, 'disable'),
        )
    enable_comment = models.IntegerField(choices=ENABLECOMMENT_CHOICES)
    objects = models.Manager() 
    # funny enough, the order matters, i.e objects before live
    # the first manager encountered is the default manager
    live = LiveBlog() 
    draft = DraftBlog() # haven't tried yet
    
    def get_absolute_url(self):
        xc = reverse('detail', args=[str(self.datetime_added.date()), str(self.title)])
        return xc
    
    def __str__(self):
        return self.title

class Image(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    