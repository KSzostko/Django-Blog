from django import forms
from django.contrib.auth.forms import UserCreationForm, get_user_model
from captcha.fields import CaptchaField
from .models import Post, Blog, Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text_content',)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('blog', 'author', 'published_date')


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'creator_photo', 'description')


class UserForm(UserCreationForm):
    captcha = CaptchaField()

    class Meta():
        model = get_user_model()
        fields = ('username', 'password1', 'password2')
