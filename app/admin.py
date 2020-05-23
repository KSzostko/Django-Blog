from django.contrib import admin
from . import models


# class UserAdmin(admin.ModelAdmin):
#     fields = ('username', 'photo')
#     list_display = ('username', 'date_joined')
#     list_filter = ('date_joined',)


# class BlogAdmin(admin.ModelAdmin):
#     fields = ('creator', 'title', 'description')
#     list_display = ('title', 'creator')
#     list_filter = ('creator',)


# class PostAdmin(admin.ModelAdmin):
#     exclude = ('published_date',)
#     list_display = ('title', 'blog', 'auth_required')
#     date_hierarchy = 'published_date'
#     list_filter = ('auth_required', 'blog')


# class CommentAdmin(admin.ModelAdmin):
#     fields = ('post', 'author', 'text_content')
#     list_display = ('post', 'author', 'text_content')
#     date_hierarchy = 'published_date'
#     list_filter = ('post', 'author')


# admin.site.register(models.Blog, BlogAdmin)
# admin.site.register(models.Post, PostAdmin)
# admin.site.register(models.Comment, CommentAdmin)
# admin.site.register(models.User, UserAdmin)
admin.site.register(models.Blog)
admin.site.register(models.Post)
admin.site.register(models.Comment)
