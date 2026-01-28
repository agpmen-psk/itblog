"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.forms import UserCreationForm
from .models import Blog
from .models import Comment 
from .forms import CommentForm, BlogForm
import re

from django.db.models import Q




def home(request):
    latest_posts = Blog.objects.order_by('-posted')[:2]  
    return render(request, "app/index.html", {
        "title": "Главная",
        "latest_posts": latest_posts,
        'year':datetime.now().year,
    })


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def links(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title':'Полезные ресурсы ',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def registration(request):
 """Renders the registration page."""
 assert isinstance(request, HttpRequest)
 if request.method == "POST": 
    regform = UserCreationForm (request.POST)
    if regform.is_valid(): 
        reg_f = regform.save(commit=False) 
        reg_f.is_staff = False 
        reg_f.is_active = True 
        reg_f.is_superuser = False
        reg_f.date_joined = datetime.now() 
        reg_f.last_login = datetime.now() 
        reg_f.save() 
        return redirect('home') 
 else:
    regform = UserCreationForm() 

 return render(
 request,
 'app/registration.html',
 {

 'regform': regform, 

 'year':datetime.now().year,
 }
 )

def blog(request):
     """Renders the blog page."""
     assert isinstance(request, HttpRequest)
     posts = Blog.objects.order_by('-posted') 
     return render(
         request,
         'app/blog.html',
         { 
         'title':'Блог',
         'posts': posts,
         'year':datetime.now().year,
         }
     )


def blogpost(request, parametr):
    """Renders the blogpost page."""
    assert isinstance(request, HttpRequest)

    post_1 = Blog.objects.get(id=parametr) 
    comments = Comment.objects.filter(post=post_1) 

    # --- похожие посты по словам в заголовке ---
    title_words = re.findall(r"[A-Za-zА-Яа-я0-9]+", (post_1.title or "").lower())
    stop = {
        "и","в","во","на","по","для","что","это","как","или","а","но","с","со","к","у","о","об","от","до","из","за","про",
        "the","a","an","to","in","on","for","and","or"
    }
    words = [w for w in title_words if len(w) >= 4 and w not in stop][:6]

    q = Q()
    for w in words:
        q |= Q(title__icontains=w)  

    related_posts = Blog.objects.none()
    if words:
        related_posts = (Blog.objects
                         .filter(q)
                         .exclude(id=post_1.id)
                         .order_by("-posted")[:4])

    # --- форма комментария ---
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user
            comment_f.date = datetime.now()
            comment_f.post = post_1
            comment_f.save()
            return redirect('blogpost', parametr=post_1.id)
    else:
        form = CommentForm()

    return render(
        request,
        'app/blogpost.html',
        {
            'post_1': post_1,
            'comments': comments,
            'form': form,
            'related_posts': related_posts,   
            'year': datetime.now().year,
        }
    )

def newpost(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)  
        if form.is_valid():
            form.save()
            return redirect("blog")  
    else:
        form = BlogForm()

    return render(request, "app/newpost.html", {"form": form, "title": "Новый пост"})

