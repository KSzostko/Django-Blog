from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('thanks', views.ThanksView.as_view(), name='thanks'),
    path('test', views.TestView.as_view(), name='test'),
    path('signup/', views.create_user, name='signup'),
    path('accounts/login/',
         auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(),
         name='logout', kwargs={'next_page': '/'}),
    path('blog/<int:pk>/', views.BlogDetailView.as_view(), name='blog_detail'),
    path('blog/new/', views.create_blog, name='blog_new'),
    path('blog/<int:pk>/post/', views.add_post, name='post_new'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/comments/',
         views.PostCommentsView.as_view(), name='post_comments'),
]
