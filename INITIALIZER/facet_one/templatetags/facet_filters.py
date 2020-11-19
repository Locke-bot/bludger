# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 11:08:32 2020

@author: Zen
"""

# Django Custom Filter

import re
import os
from django.conf import settings
from django import template
import os
from comments.models import UserComment, CommentLikes
from facet_one.models import Blog
register = template.Library()

@register.filter()
def index(collection, index):
    return collection[index]

@register.filter()
def comments_reply(comment, user=""):
    step = 20
    # for the first time, it will be visible, the rest will be visible only when the shots are called
    def recursive_reply(comment, blog, count=0, output=[], comment_possible=False):
        current = comment.text 
        maximi = UserComment.objects.filter(reply__id=comment.id, blog=blog)[::-1]
        output += [comment_reply_template(comment, count, step, len(maximi), user)]
        count += 1
        for i, maxi in enumerate(maximi):
            output = recursive_reply(maxi, blog, count, output) 
        return output
    i = comment
    rev = recursive_reply(i, i.blog) 
    # only the original comment to the blog will be visible on start-up
    # return defoe 
    x = [i for i in CommentLikes.objects.filter(user__username="Cynic")[0].comment.all()]
    return ''.join(rev) # no worries textareas display will be set to block

def comment_reply_template(comment, value, step, children, user):
    # no need to filter with respect to comment and blog
    # if uniqueness is sought after, comment id is unique cross border,
    # since one comment model serves all blogs
    text = comment.text
    id_  = comment.id
    reply_button = f'<a role="button" style="margin-left: {value*step}px" class="commentReply smallfont">Reply</a>'
    author = comment.author 
    time_added = comment.comment_added 
    like = comment.likes
    disabled = "disabled"
    is_checked = ""
    if type(user) is not str:
        checked = CommentLikes.objects.filter(comment=comment, user=user) # if empty it's not checked
        disabled = "" # only users(logged in folks) can like comments 
        if checked: is_checked="checked"
    check_like = f'<input type="checkbox" type="submit" {is_checked} {disabled} class="likeButton">'
    time_added = time_added.strftime("%b. %d, %Y, %I:%S %p")
    comment_specs = f'<span style="margin-left: 10px" class="commentSpecs smallfont">\
        &nbsp;<span class="dotfont">&centerdot;</span> \
        <span class="author">{author}</span>&nbsp;&nbsp;\
        <span class="dotfont">&centerdot;</span><span class="commentTime">{time_added}.</span>\
        &nbsp;&nbsp;<span class="dotfont">\
        &centerdot;</span> <span class="likes">{check_like} <span class="likelabel"\
        >{like} {"likes" if int(like) > 1 else "like"}</span></span></span>'
        
    # value == 0        
    status = "see"
    if children > 1:
        inner = f"{status} all {children} replies"
    elif children == 1:
        inner = f"{status} 1 reply"
    else: 
        inner = ""
    collapse_button = f'<a role="button" style="margin-left: 10px" class="smallfont collapser">{inner}</a>' 
    # collapse is already used 
    # hide means how many parents will be viewed 'fore it can be
    # hide = 0 means all the necessary ancestors have been taken care of
    # meaning it will all be visible immediately no matter the nesting
    # for example, if hide = 1, it will all be hidden, even the "original"
    # comments, that's why it must be dynamic, say value based.
    textarea =  f'<span hide={value} nest={value}><textarea disabled class="usercomment" cols="40" readonly \
    name={id_} style="margin-left: {value*step}px">{text}</textarea>{reply_button}{collapse_button}{comment_specs}</span>'
    return textarea
    
@register.filter() 
def check_css(value, klass): # css klass being checked for.
    value = str(value) 
    raw = r'\s*?<.*?class\s*?=\s*?.*?\b{}\b.*?.*?>\s*?'.format(klass)
    regex = re.compile(raw)
    return bool(regex.findall(value))

@register.filter(is_safe=True)
def add_css(value, attr):
    attr = attr.split(',')
    value = str(value) 
    if not value.strip():
        return
    if not attr:
        return value
    if len(attr) == 1:
        attr, attr_value = attr[0], None
    elif len(attr) == 2:
        attr, attr_value = attr[0], attr[1]
    # not very accurate(matching quotes and all), but it will get the job down. 
    raw = r'\b({attr})\s*?(=)?'.format(attr=attr) + '(?(2)(\'|\")(.*?)(\'|\"))'
    regex = re.compile(raw) 
    css = regex.findall(value)
    if css:
        css = css[0]
        css = [css[0], ''.join(css[2:])] # to bypass the =
        if not css[1].strip(): # empty attribute
            css[1] = '"'
        if css[0] == 'class':
            if css[1]:
                quote = css[1][0]
                class_fields = css[1][1:-1].split(' ') # removing the quotes
                if attr_value is not None:
                    if attr_value not in class_fields:
                        class_fields.append(attr_value)
                        value = regex.sub('class={}'.format(quote+" ".join(class_fields)+quote), value)
                        return value
                    else:
                        return value
        else: # overwrite
            quote = css[1][0]
            if attr_value is not None:
                return regex.sub('{}={}'.format(css[0], quote+attr_value+quote), value)
    else: # no such attribute, must be created
        index = value.index('>') # the first one
        if not index:
            raise ValueError('index of the first closing tag cannot be zero')
        if value[index-1] != ' ':
            value = value[:index]+' '+value[index:]
            index += 1
        if attr_value is not None:
            attr += f'="{attr_value}"' 
        value = value[:index] + attr + value[index:]
        return value

@register.filter()
def summary_blog(value):
    breaks = ["<img", "<pre"] # cut it off at image or pre tags, or for pre substitute it with <p tags
    regex = re.compile('|'.join(breaks)) 
    try:
        index = regex.finditer(value).__next__().start()
    except StopIteration:
        w = min(len(value), 220) 
        return value[:w]
    else:
        w = min(index, 220)
        return value[:w]

@register.filter()
def modulus(value, arg):
    arg = int(arg)
    return value%arg

@register.filter()
def dirs(value):
    return dir(value)

@register.filter()
def check_attr(value, attr):
    if hasattr(value, 'field'):
        value = str(value.field)
    value = str(value)
    # not class
    # regex = re.compile(r'\b{}\s*?=\s*?(?:\'|\")(.*?)(?:\'|\")\b'.format(attr)) 
    regex = re.compile(r'\b{}\s*?=\s*?(?:\"|\')(\w+)(?:\"|\')'.format(attr)) 
    matches = regex.findall(value) or [""]
    return matches[0]    
