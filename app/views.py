"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.forms import UserCreationForm
from .models import Blog
from .models import Comment # использование модели комментариев
from .forms import CommentForm, BlogForm


def home(request):
    latest_posts = Blog.objects.order_by('-posted')[:2]  # если поле даты другое — поменяй тут
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
 if request.method == "POST": # после отправки формы
    regform = UserCreationForm (request.POST)
    if regform.is_valid(): #валидация полей формы
        reg_f = regform.save(commit=False) # не сохраняем автоматическиданные формы
        reg_f.is_staff = False # запрещен вход в административный раздел
        reg_f.is_active = True # активный пользователь
        reg_f.is_superuser = False # не является суперпользователем
        reg_f.date_joined = datetime.now() # дата регистрации
        reg_f.last_login = datetime.now() # дата последней авторизации
        reg_f.save() # сохраняем изменения после добавления данных (добавление пользователя в БД пользователей)
        return redirect('home') # переадресация на главную страницу после регистрации
 else:
    regform = UserCreationForm() # создание объекта формы для ввода данных нового пользователя

 return render(
 request,
 'app/registration.html',
 {

 'regform': regform, # передача формы в шаблон веб-страницы

 'year':datetime.now().year,
 }
 )

def blog(request):
     """Renders the blog page."""
     assert isinstance(request, HttpRequest)
     posts = Blog.objects.order_by('-posted') # запрос на выбор всех статей из модели, отсортированных по убыванию даты опубликования
     return render(
         request,
         'app/blog.html',
         { # параметр в {} — данные для использования в шаблоне.
         'title':'Блог',
         'posts': posts, # передача списка статей в шаблон веб-страницы 
         'year':datetime.now().year,
         }
     )

def blogpost(request, parametr):
     """Renders the blogpost page."""
     assert isinstance(request, HttpRequest)
     post_1 = Blog.objects.get(id=parametr) # запрос на выбор конкретной статьи по параметру
     comments = Comment.objects.filter(post=parametr)
     if request.method == "POST": # после отправки данных формы на сервер методом POST
         form = CommentForm(request.POST)
         if form.is_valid():
             comment_f = form.save(commit=False)
             comment_f.author = request.user # добавляем (так как этого поля нет в форме) в модель Комментария (Comment) в поле автор авторизованного пользователя
             comment_f.date = datetime.now() # добавляем в модель Комментария (Comment) текущую дату
             comment_f.post = Blog.objects.get(id=parametr) # добавляем в модель Комментария (Comment) статью, для которой данный комментарий
             comment_f.save() # сохраняем изменения после добавления полей

             return redirect('blogpost', parametr=post_1.id) # переадресация на ту жестраницу статьи после отправки комментария
     else:
         form = CommentForm() # создание формы для ввода комментария

     return render(
         request,
         'app/blogpost.html',
         {
       'post_1': post_1, # передача конкретной статьи в шаблон веб-страницы
       'comments': comments, # передача всех комментариев к данной статье в шаблон веб-страницы
       'form': form, # передача формы в шаблон веб-страницы
     'year':datetime.now().year,
     }
 )

def newpost(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)  # важно для загрузки файлов
        if form.is_valid():
            form.save()
            return redirect("blog")  # или куда тебе надо после публикации
    else:
        form = BlogForm()

    return render(request, "app/newpost.html", {"form": form, "title": "Новый пост"})

