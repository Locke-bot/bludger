# -*- coding: utf-8 -*-
from facet_one import models as facet_one_models

# I should be very careful, if the url changes, use a url as the descriptor to forestall imtegrity error
# due to attempts to save different urls with the same descriptors, descriptors are unique, 
# or should they, I will remove the uniquenesss part, I will just have to be careful myself,
# take confirm email for example, it still is confirm email but the appended slug varies, 
# will remove the uniqueness of descriptors now.

# Now that I know better, I should have created a middleware for this, it's way cleaner
# a very good interceptor 

def addToURLModel(descriptor="", format=None, eval_=False): # format should be a collection not a mapping 
    def inner(function):
        import functools
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            import datetime
            descript = descriptor
            global request 
            request = args[0]
            if format is not None:
                # eval_ only has significance when format is not None
                if eval_:
                    descript = descript.format(*[eval(i) for i in format])
                else:
                    descript = descript.format(*format)
            if hasattr(request, "request"): # then it's a method with args[0] as self
                # I should just check the class tho
                request = request.request
                if request.is_ajax() and (request.POST.get("name") in ("likes", "comment")):
                        return function(*args, **kwargs)
            path = request.path
            link = facet_one_models.Url.objects.filter(url=request.path) 
            date = datetime.date.today() # safer, we gotta refer to the same date, just an edge case though.
            url_count = facet_one_models.UrlCount.objects.get_or_create(date=date, Url=request.path, defaults={'description':descript}) 
            # filters = facet_one_models.UrlCount.objects.filter(Url=request.path)[0]
            # a get search won't entail the inmates of defaults
            url_count = url_count[0] 
            # get_or_create returns a tuple of the instance and whether the object 
            # was created or not, True if created.
            if not link:
                facet_one_models.Url.objects.create(url=request.path, descriptor=descript,
                                                    url_visit_count=url_count)
                
            url_count.count += 1
            url_count.save()
            visits = facet_one_models.LinksVisit.objects.get_or_create(today_date=date)[0] 
            visits.no_of_visits += 1
            visits.save() 
            return function(*args, **kwargs) 
        return wrapper
    return inner

