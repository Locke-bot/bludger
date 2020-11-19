from django.http import request
from django.contrib import admin
from .models import Blog, LinksVisit, Url, UrlCount
from django.utils.safestring import mark_safe
from comments.models import UserComment
# Register your models here.

class CommentInline(admin.TabularInline):
    model = UserComment
    extra = 0

class Blogger(admin.ModelAdmin):
    list_display = ('author', 'title', 'datetime_added', 'last_updated', 'blog_image_show')
    list_display_links = list_display
    
    def blog_image_show(self, obj):
        if obj.blog_image:
            return mark_safe(f"<img src={obj.blog_image.url} height=150>")
        else:
            return '-'
    blog_image_show.short_description = "blog image"
    
    ordering = ['-last_updated']
    inlines = [CommentInline]
    save_on_top = True
    view_on_site = True
    
        
class LinksVisitor(admin.ModelAdmin):
    pass
    
class UrlClass(admin.ModelAdmin):
    list_display = ('descriptor', 'url')

class UrlCounter(admin.ModelAdmin):
    list_display = ("description", "date", "count")
    
admin.site.register(UrlCount, UrlCounter)
admin.site.register(Url, UrlClass)
admin.site.register(LinksVisit, LinksVisitor)
admin.site.register(Blog, Blogger)

