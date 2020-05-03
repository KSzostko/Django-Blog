from django.shortcuts import render
from django.http import HttpResponse
from .models import Blog

# Create your views here.


def index(request):
    context = {'blog_list': Blog.objects.all()}
    return render(request, 'index.html', context=context)
