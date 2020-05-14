from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blog/<int:pk>/', views.BlogDetailView.as_view(), name='blog_detail'),
    path('blog/new/', views.CreateBlogView.as_view(), name='blog_new'),
    path('blog/<int:pk>/post/', views.add_post, name='post_new'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/comments/',
         views.CommentListView.as_view(), name='comment_list'),
]
