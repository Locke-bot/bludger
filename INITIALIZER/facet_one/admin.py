from django.contrib import admin
from django.utils.safestring import mark_safe
from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group
from .models import Blog, LinksVisit, Url, UrlCount
from comments.models import UserComment
# Register your models here.

class StaffAdmin(AdminSite):
    site_header = 'Staff Admin'
    
StaffAdmin = StaffAdmin(name='StaffAdmin')

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
    
    def has_add_permission(self, request):
        user = request.user
        if user.has_perm('facet_one.add_blog'):
            return True

    def has_change_permission(self, request, obj=None):
        user = request.user
        print('plk', self.readonly_fields)
        if not user.has_perm('facet_one.change_blog'):
            return False
        if user.is_superuser or obj is None:
            return True
        if isinstance(obj, Blog) and Group.objects.get(name='Staff') in user.groups.all() and obj.author == user:
            return True
        return False
        # if user.has_perm('facet_one.add_blog') and user.is_staff and 
        
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

StaffAdmin.register(Blog, Blogger)