from django.contrib import admin
from .models import UserComment, CommentLikes
# from django.utils.safestring import mark_safe

# Register your models here.

class UserCommentClass(admin.ModelAdmin):
    list_display = ("text", "author", "comment_added", "likes")
    list_display_links = list_display[:-1]

class UserCommentLikes(admin.ModelAdmin):
    pass    
    
admin.site.register(CommentLikes, UserCommentLikes)
admin.site.register(UserComment, UserCommentClass) 

