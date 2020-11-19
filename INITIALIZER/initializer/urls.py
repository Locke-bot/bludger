"""initializer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static # new
from facet_one import views as one_views

urlpatterns = [
    # when the admin url is changed, a change has to be made to the url used in the url_fieldset_js.js file
    path(f'{settings.ADMIN_URL}/', admin.site.urls),
    url(r'^$',one_views.HomePageView, name='homepage'),
    url(r'^articles/(?P<page>\d+)/', one_views.ListBlogPost.as_view(), name='articles'),
    url(r'blog/(?P<date_created>[\d-]+)/(?P<blog_name>\w+)/', one_views.DetailPageView.as_view(), name='detail'),
    url(r'blog/(?P<date_created>[\d-]+)/(?P<blog_name>\w+)/', one_views.DetailPageView.as_view(), name='detail'),
    url(r'^blog/random/', one_views.RandomBlogView, name='random'),
    url(r'^about/', include('facet_one.urls', namespace='about')), 
    url('^accounts/', include('allauth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG and False:
    import debug_toolbar
    urlpatterns = [ 
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns