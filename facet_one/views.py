import random
import math
import datetime
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView 
from django.views.generic.edit import FormMixin
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import TemplateView
from django.contrib.auth.models import User

from .form import SignInForm
from .models import Blog, Url, UrlCount, LinksVisit, Staff
from comments.models import UserComment, CommentLikes
from comments.form import CommentForm

# from django import contrib
def RandomBlogView(request):
    model = Blog
    blog_list = random.choice(model.live.all())
    args = (blog_list.datetime_added.date(), blog_list.title,) 
    return HttpResponseRedirect(reverse('detail', args=args)) 
    
class ListBlogPost(ListView):
    model = Blog
    template_name = 'bloglist.html'
    context_object_name = 'object_list'
    paginate_by = 2
    queryset = model.live.order_by('-datetime_added') 
    count = queryset.count()
    no_of_pages = math.ceil(count/paginate_by)
    
    def get_context_data(self, **kwargs):
        path = self.request.path
        kwargs['url'] = path
        path_list = path.split('/')
        kwargs['page'] = int(path_list[-2])
        path_list[-2]  = str(int(path_list[-2]) + 1) # subtract in f expression below
        kwargs['url_next'] = '/'.join(path_list)
        kwargs['pages'] = list(range(1, self.no_of_pages+1))
        kwargs['no_of_pages'] = self.no_of_pages
        return super().get_context_data(**kwargs)

class DetailPageView(FormMixin, DetailView): 
    model = Blog
    template_name = 'blog_detail.html'
    form_class = CommentForm
    slug_url_kwarg = 'date_created'
    slug_field = 'datetime_added__date'
    
    
    def get_queryset(self):
        kwargs = self.kwargs
        print("QEDED", self.kwargs, self.template_name)
        # not the right way by a long shot but it should do. 
        return self.model.live.filter(title__iexact=kwargs['blog_name']).all()

    def get_success_url(self):
        return self.model.get_success_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        initial={'blog': self.object}
        if self.request.user.is_authenticated:
            initial["author"] = self.request.user
        context['form'] = CommentForm(initial=initial) 
        return context
 
    def post(self, request, *args, **kwargs):
        self.object = self.get_object() 
        if self.request.is_ajax():
            print("DICO")
            dico = request.POST
            print(dico)
            if dico.get("name") == "likes":
                try:
                    x = CommentLikes.objects.filter(user=request.user)[0]
                except IndexError:
                    x =  CommentLikes.objects.create(user=request.user, liked=True)
                    x.comment.add(UserComment.objects.get(pk=dico["pk"]))
                else:
                    if dico["status"] == "false":
                        x.comment.remove(UserComment.objects.get(pk=dico["pk"])) 
                        x.save()
                    elif dico["status"] == "true":
                        x.comment.add(UserComment.objects.get(pk=dico["pk"]))
                        x.save() 
                    
            elif dico.get("name") == "comment":
                if eval(dico['parent_id']) is not None:
                    x = UserComment.objects.create(text=dico['text'], author=request.user,
                                        blog=self.object, reply=UserComment.objects.get(pk=int(dico['parent_id'])))
                else:
                    x = UserComment.objects.create(text=dico['text'], author=request.user,
                                        blog=self.object)
                time_added = x.comment_added
                time_added = time_added.strftime("%b. %d, %Y, %I:%S %p")
                data = {
                        'pk': x.id,
                        'time_added': time_added,
                        'username': x.author.username,
                    }
                return JsonResponse(data)
            
            elif dico.get('name') == 'search_blog':
                search_text  = dico['search_text']  
                x = Blog.live.filter(title__icontains = search_text).all()
                titles = [i.title for i in x]
                urls = [i.get_absolute_url() for i in x]
                data = {
                        'search_results': titles,
                        'urls': urls,
                    }
                return JsonResponse(data)
            
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form) 
        else:
            return self.form_invalid(form)
    
    def form_valid(self, form):
        form.save() 
        return super().form_valid(form)  
    
def AboutPageView(request, page_id=0):
    details = {'page_id':page_id}
    return render(request, 'about.html', details)

def HomePageView(request):
    no_of_blogs = 3 # number of blogs shown in the homepage at startup 
    queryset = Blog.live.order_by('datetime_added')[:min(Blog.live.count(), no_of_blogs)]
    return render(request, 'homepage.html', {'recent_posts':queryset})