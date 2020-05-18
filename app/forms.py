from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Blog


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('blog', 'author', 'published_date')


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'description')


class UserForm(UserCreationForm):
    model = get_user_model()
    fields = ('username', 'photo', 'password1', 'password2')

    # def __init__(self, *args, **kwargs):
    # super.__init__(*args, **kwargs)
