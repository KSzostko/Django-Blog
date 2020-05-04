from django.shortcuts import render
from django.views import generic
from .models import Blog

# Create your views here.


def index(request):
    context = {'blog_list': Blog.objects.all()}
    return render(request, 'index.html', context=context)


class BlogView(generic.DetailView):
    model = Blog
    template_name = 'blog_detail.html'
