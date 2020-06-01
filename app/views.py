from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from .models import Blog, Post, Comment
from django.contrib.auth.models import User
from .forms import PostForm, BlogForm, UserForm, CommentForm

# Create your views here.


def index(request):
    context = {'blog_list': Blog.objects.all()}
    return render(request, 'app/index.html', context=context)


@login_required
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

    return render(request, 'app/post_form.html', context={'form': form, 'author': blog.creator})


def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            user = form.save()
            # send_mail(
            #     'Welcome!',
            #     'Welcome to our fantastic Bloggers Community! We hope you will stay here for a while',
            #     'email host',
            #     [user.email, ],
            # )

            return redirect('index')
    else:
        form = UserForm()

    return render(request, 'app/signup.html', context={'form': form})


class BlogDetailView(generic.DetailView):
    model = Blog
    template_name = 'app/blog_detail.html'


@login_required
def create_blog(request):
    user = User.objects.get(pk=request.user.pk)

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)

        if form.is_valid():
            blog = form.save(commit=False)

            blog.creator = user
            blog.save()

            return redirect('index')
    else:
        form = BlogForm()

    return render(request, 'app/blog_form.html', context={'form': form})


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'app/post_detail.html'


class UpdatePostView(LoginRequiredMixin, generic.UpdateView):
    login_url = '/login/'
    model = Post
    form_class = PostForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.kwargs.get('pk')})


class DeletePostView(LoginRequiredMixin, generic.DeleteView):
    login_url = '/login/'
    model = Post

    def get_success_url(self):
        post = super().get_object()
        return reverse_lazy('blog_detail', kwargs={'pk': post.blog.pk})


class SearchPostsView(generic.ListView):
    model = Post
    template_name = 'app/posts_search.html'

    def get_queryset(self):
        title = self.request.GET.get('title')
        blog = self.request.GET.get('blog')
        auth = self.request.GET.get('auth')

        objects = Post.objects.all()

        if blog == '':
            if auth == 'both':
                return Post.objects.filter(
                    title__icontains=title,
                )
            else:
                auth = auth == 'True'
                return Post.objects.filter(
                    title__icontains=title,
                    auth_required=auth
                )
        else:
            if auth == 'both':
                return Post.objects.filter(
                    title__icontains=title,
                    blog__id=blog,
                )
            else:
                auth = auth == 'True'
                return Post.objects.filter(
                    title__icontains=title,
                    blog__id=blog,
                    auth_required=auth
                )


@login_required
def add_comment(request, pk):
    user = User.objects.get(pk=request.user.pk)
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)

            comment.post = post
            comment.author = user
            comment.save()

            return redirect('post_detail', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'app/post_comments.html', {'object': post, 'form': form})


class ThanksView(generic.TemplateView):
    template_name = 'app/thanks.html'


class TestView(generic.TemplateView):
    template_name = 'app/test.html'
