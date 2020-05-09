from django.shortcuts import render
from django.views import generic
from .models import Blog, Post

# Create your views here.


def index(request):
    context = {'blog_list': Blog.objects.all()}
    return render(request, 'index.html', context=context)


class BlogDetailView(generic.DetailView):
    model = Blog
    template_name = 'blog_detail.html'


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'
