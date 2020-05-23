from django.contrib import admin
from . import models


class BlogAdmin(admin.ModelAdmin):
    fields = ('creator', 'creator_photo', 'title', 'description')
    list_display = ('title', 'creator')
    list_filter = ('creator',)


class PostAdmin(admin.ModelAdmin):
    exclude = ('published_date',)
    list_display = ('title', 'blog', 'auth_required')
    date_hierarchy = 'published_date'
    list_filter = ('auth_required', 'blog')


class CommentAdmin(admin.ModelAdmin):
    fields = ('post', 'author', 'text_content')
    list_display = ('post', 'author', 'text_content')
    date_hierarchy = 'published_date'
    list_filter = ('post', 'author')


admin.site.register(models.Blog, BlogAdmin)
admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Comment, CommentAdmin)
