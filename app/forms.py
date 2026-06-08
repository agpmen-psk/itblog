from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Blog, Comment, Order


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Логин")
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput
    )


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ("title", "description", "content", "image")
        labels = {
            "title": "Заголовок",
            "description": "Краткое содержание",
            "content": "Полное содержание",
            "image": "Изображение",
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)
        labels = {
            "text": "Комментарий",
        }
        widgets = {
            "text": forms.Textarea(attrs={"rows": 4}),
        }


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("comment",)
        labels = {
            "comment": "Комментарий к заказу",
        }
        widgets = {
            "comment": forms.Textarea(attrs={"rows": 4}),
        }