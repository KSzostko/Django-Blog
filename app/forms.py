from django import forms
from .models import Post, Blog


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('blog', 'author', 'published_date')


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'description')
