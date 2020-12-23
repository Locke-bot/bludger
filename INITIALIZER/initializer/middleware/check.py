# -*- coding: utf-8 -*-
import datetime
import re
from facet_one import models as facet_one_models
from django.conf import settings

class VisitCountMiddleware:
    ''' A middleware class to log access to urls within the project '''
    
    def __init__(self, get_response):
        self.get_response  = get_response
        
    def __call__(self, request):
        
        response = self.get_response(request)

        # don't trigger a visit count for likes and comments 
        # should I care about say GET request only, because for instance, when the allauth 
        # login page is accessed, there are 2 visits counts, one for the GET and POST request
        # one is a 200, the other is a 302, I should just let it lie though
        if request.is_ajax() and (request.POST.get("name") in ("likes", "comment")):
                return response
        
        url = request.path
            
        def desc(*, format=None, args=None, constant=None, url_re=None):
            # change the outer function url variable
            nonlocal url
            if constant is not None:
                url = url_re.pattern
                regex = re.compile(r'\(|\)|\^|')
                url = regex.sub('', url)
                return constant
            if args is not None:
                captures = list(url_re.findall(request.path)[0]) 
                url = captures.pop(0) # to remove the first whole capture
                args = (captures[i] for i in args)
                out = format.format(*args)
                return out
            return format # almost like constant see, don't wanna raise an error
        
        descript_urls = { # by static, I mean those like homepage, and dynamic would be those like the detail page
                '/': 'Home page',
                '/about/': 'About page',
                '/accounts/login/': 'Login page',
                '/accounts/logout/': 'Logout page',
                '/accounts/signup/': 'Signup page',
                '/blog/random/': 'Random page',
            } 
        
        # put the more specialized ones up in the list, the first match will be used
        # should use a LRU cache though, some pages tend to be more frequently accessed
        # than others
        
        dynamic_urls_re = [
                re.compile(r'(^/blog/([-\d]+)/(\w+)/$)'), # for the DetailViewPage class
                re.compile(r'(^/articles/(\d+)/$)'), # For the articles page (Explore link)
                re.compile(r'(^/accounts/confirm-email/(\S+)/$)'), # email-confirm page
                re.compile(rf'(^/{settings.SUPERUSER_ADMIN_URL}/)'), # Group all admin pages together, don't need the details, coerce urls back to this
                re.compile(rf'(^/{settings.STAFF_ADMIN_URL}/)'), # Group all admin pages together, don't need the details, coerce urls back to this
                re.compile(rf'(^{settings.MEDIA_URL})'),
                re.compile(rf'(^{settings.STATIC_URL})'),
            ]
            
        dynamic_urls_args = [
                {'format': 'Blog Detail Page - {}', 'args':(1,)}, # which is the second capture of the regex 
                {'format': 'Articles Page - {}', 'args':(0,)},
                {'constant': 'Email confirmation'},
                {'constant': 'admin'},
                {'constant': 'staff_admin'},
                {'constant': 'media'},
                {'constant': 'static'},
            ]
    
        descript = descript_urls.get(request.path, None)
        if descript is None:
            for i, url_re in enumerate(dynamic_urls_re):
                if url_re.findall(request.path):
                    working_copy = dict(dynamic_urls_args[i]) 
                    # this gives that both dynamic lists must be of the same length
                    working_copy['url_re'] = url_re
                    descript = desc(**working_copy)
                    break
            else:
                descript = request.path 
        
        link = facet_one_models.Url.objects.filter(url=url) 
        date = datetime.date.today() # safer, we gotta refer to the same date, just an edge case though.
        url_count = facet_one_models.UrlCount.objects.get_or_create(date=date, Url=url, defaults={'description':descript})[0]
        # a get search won't entail the inmates of defaults
        # get_or_create returns a tuple of the instance and whether the object 
        # was created or not, True if created.
        if not link:
            facet_one_models.Url.objects.create(url=url, descriptor=descript,
                                                url_visit_count=url_count)

        url_count.count += 1
        url_count.save()
        
        visits = facet_one_models.LinksVisit.objects.get_or_create(today_date=date)[0] 
        visits.no_of_visits += 1
        visits.save()         
        
        return response 