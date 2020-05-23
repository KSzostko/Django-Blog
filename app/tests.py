from django.test import TestCase
from django.urls import reverse
from . import models


def create_user(username):
    return models.User.objects.create(username=username, password='testpassword')


def create_blog(user, title, description):
    return models.Blog.objects.create(creator=user, title=title, description=description)


def create_post(blog, author, title, text_content, auth_required):
    return models.Post.objects.create(blog=blog, author=author, title=title, text_content=text_content, auth_required=auth_required)


class BlogModelTests(TestCase):

    def test_no_blogs(self):
        """
        If no blogs exist, an appropriate message is displayed
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "There are currently no blogs started :(")

    def test_one_blog(self):
        """
        If there's a blog, info about it will be displayed
        """
        create_blog(create_user('anon'), 'Title', 'Blog description')

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['blog_list'],
            ['<Blog: Title>']
        )

    def test_blog_creator_name(self):
        """
        If there's a blog, creator name will be displayed
        """
        create_blog(create_user('anon'), 'Title', 'Blog description')

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'created by: anon')

    def test_blog_title(self):
        """
        If there's a blog, blog title will be displayed
        """
        create_blog(create_user('anon'), 'My title', 'Blog description')

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'My title')

    def test_blog_description(self):
        """
        If there's a blog, blog description will be displayed
        """
        create_blog(create_user('anon'), 'My title', 'Blog description')

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Blog description')


class PostModelTests(TestCase):

    def test_no_posts(self):
        """
        If there's no posts on a blog, an appropriate message is displayed
        """
        user = create_user('anon')
        blog = create_blog(user, 'Blog title', 'Blog description')

        response = self.client.get(reverse('blog_detail', args=(blog.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, 'Currently, there are no posts created yet')

    def test_one_post(self):
        """
        If there's a post on the blog, info about it will be displayed
        """
        user = create_user('anon')
        blog = create_blog(user, 'Blog title', 'Blog description')

        create_post(blog, user, 'Post title', 'Post content', False)

        response = self.client.get(reverse('blog_detail', args=(blog.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['object'].post_set.all(),
            ['<Post: Blog title: Post title>'],
        )
