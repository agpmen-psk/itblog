"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.db import models
from.models import Comment, Blog

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {'text': "Комментарий"}
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control bober-textarea',
                'rows': 6,
                'placeholder': 'Что думаешь? (без флуда, но с фактами)',
            }),
        }

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ("title", "description", "image", "content")
        labels = {
            "title": "Заголовок",
            "description": "Краткое содержание",
            "image": "Картинка",
            "content": "Полное содержание",
        }
        widgets = {
            "excerpt": forms.Textarea(attrs={"rows": 3}),
            "content": forms.Textarea(attrs={"rows": 10}),
        }

