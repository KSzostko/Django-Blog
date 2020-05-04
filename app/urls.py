from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.BlogView.as_view(), name='blog_detail'),
]
