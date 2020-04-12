from django.db import models
from django.contrib import auth
from django.utils import timezone


class User(auth.models.User):

    def __str__(self):
        return f'{self.username}'


class Blog(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.title}'


class Post(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text_content = models.TextField()
    image = models.ImageField(blank=True)
    auth_required = models.BooleanFiled(default=False)
    published_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.blog}{self.title}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text_content = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)
