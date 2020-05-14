from django.shortcuts import render
from django.views import generic
from .models import Blog, Post, Comment
from .forms import PostForm

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


class CreatePostView(generic.CreateView):
    redirect_field_name = 'blog_detail.html'
    template_name = 'post_form.html'
    form_class = PostForm
    model = Post


class CommentListView(generic.ListView):
    model = Comment
    template_name = 'comment_list.html'
