from django.db import models
from django.contrib.auth import get_user_model
from facet_one.models import Blog
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
# Create your models here.
# XoXo

class UserComment(models.Model):
    text = models.TextField(blank=True, default="")
    # for this author, I am conflicted, say a user deletes his account, 
    # must I then, delete his comments, nah is what I think.
    author = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    comment_added = models.DateTimeField(auto_now_add=True, verbose_name="comment added")
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True) 
    likes = models.PositiveIntegerField(blank=True, default=0)
    
    class Meta: 
        default_permissions = ('add',)
        
    def model_name(self):
        return str(type(self).__name__)
        
    def __str__(self):
        txt = self.text[:min(len(self.text), 30)]
        return f'comment, blog: {txt}... [{self.blog.title}] [{self.id}]'
    
    
class CommentLikes(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.PROTECT)
    comment = models.ManyToManyField(UserComment)
    liked = models.BooleanField()
    
    class Meta:
        verbose_name_plural = "Comment Likes"
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def __str__(self):
        return str(self.user) 
    
    def model_name(self):
        return str(type(self).__name__)
    
@receiver(m2m_changed, sender=CommentLikes.comment.through)
def comment_changed(sender, **kwargs):
    action = kwargs["action"]
    if action in ("post_remove", "post_add",):
        for pk in kwargs["pk_set"]:
            comment = UserComment.objects.filter(pk=pk)[0]
            # u making every iteration, not efficiently, just check the first time;
            # premature optimization is the root of most evil tho.
            if action == 'post_remove': comment.likes -= 1
            elif action == "post_add": comment.likes += 1
            comment.save()
 
