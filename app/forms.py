from django import forms
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import CaptchaField
from .models import Post, Blog, User, Comment


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
        fields = ('title', 'description')


class UserForm(UserCreationForm):
    captcha = CaptchaField()

    class Meta():
        model = User
        fields = ('username', 'photo', 'password1', 'password2')

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.fields['photo'].label = 'A teraz to pewnie zadzialasz'
            # for fieldname in ['username', 'photo', 'password1', 'password2']:
            # self.fields['username'].help_text = ''
