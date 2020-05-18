from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Blog, Post, Comment, User
from .forms import PostForm, BlogForm, UserForm

# Create your views here.


def index(request):
    context = {'blog_list': Blog.objects.all()}
    return render(request, 'index.html', context=context)


def add_post(request, pk):
    blog = get_object_or_404(Blog, pk=pk)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)

            post.blog = blog
            post.author = blog.creator
            post.save()

            return redirect('blog_detail', pk=blog.pk)
    else:
        form = PostForm()

    return render(request, 'post_form.html', context={'form': form})


def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            return redirect('index')
    else:
        form = UserForm()

    return render(request, 'signup.html', context={'form': form})


class BlogDetailView(generic.DetailView):
    model = Blog
    template_name = 'blog_detail.html'


class CreateBlogView(generic.CreateView, LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'index.html'
    template_name = 'blog_form.html'
    form_class = BlogForm
    model = Blog


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'


class PostCommentsView(generic.DetailView):
    model = Post
    template_name = 'post_comments.html'
