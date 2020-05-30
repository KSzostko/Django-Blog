from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from . import models


def create_user(username):
    return User.objects.create_user(username=username, password='testpassword')


def create_blog(user, title, description):
    return models.Blog.objects.create(creator=user, title=title, description=description)


def create_post(blog, author, title, text_content, auth_required):
    return models.Post.objects.create(blog=blog, author=author, title=title, text_content=text_content, auth_required=auth_required)


def create_comment(post, author, text_content):
    return models.Comment.objects.create(post=post, author=author, text_content=text_content)


class IndexViewTests(TestCase):

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


class BlogDetailViewTests(TestCase):
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

    def test_one_auth_post_user_not_logged(self):
        """
        If there's a private post on the blog (auth_required=True),
        not authenticated user wont' see it
        """
        user = create_user('anon')
        blog = create_blog(user, 'Blog title', 'Blog description')

        create_post(blog, user, 'Post title', 'Post content', True)

        response = self.client.get(reverse('blog_detail', args=(blog.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, 'Only logged members can see post')

    def test_one_auth_post_one_not_user_not_logged(self):
        """
        If there's a private and non-private post on the blog,
        not authenticated user will see only non-private post 
        """
        user = create_user('anon')
        blog = create_blog(user, 'Blog title', 'Blog description')

        create_post(blog, user, 'Post title', 'Post content', True)
        create_post(blog, user, 'Second title', 'Second Post content', False)

        response = self.client.get(reverse('blog_detail', args=(blog.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, 'Second title')
        self.assertContains(
            response, 'Only logged members can see post: Post title')

    def test_one_auth_post_user_logged(self):
        """
        If there's a private post on the blog (auth_required=True),
        authenticated user wil see it anyway
        """
        user = create_user('anon')
        blog = create_blog(user, 'Blog title', 'Blog description')

        create_post(blog, user, 'Post title', 'Post content', True)

        self.client.login(username='anon', password='testpassword')
        response = self.client.get(reverse('blog_detail', args=(blog.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['object'].post_set.all(),
            ['<Post: Blog title: Post title>'],
        )

    def test_one_auth_post_one_not_user_logged(self):
        """
        If there's a private and non-private post on the blog,
        authenticated user will see both posts 
        """
        user = create_user('anon')
        blog = create_blog(user, 'Blog title', 'Blog description')

        create_post(blog, user, 'Post title', 'Post content', True)
        create_post(blog, user, 'Second title', 'Second Post content', False)

        self.client.login(username='anon', password='testpassword')
        response = self.client.get(reverse('blog_detail', args=(blog.id,)))
        self.assertEqual(response.status_code, 200)

        posts_list = list(response.context['object'].post_set.all())
        self.assertQuerysetEqual(
            posts_list,
            ['<Post: Blog title: Post title>', '<Post: Blog title: Second title>'],
        )

    def test_not_creator_add_post(self):
        """
        If authenticated user is not blog creator, he won't see button for adding new post
        """
        user = create_user('anon')

        author = create_user('anon2')
        blog = create_blog(author, 'Blog title', 'Blog description')

        self.client.login(username='anon', password='testpassword')
        response = self.client.get(reverse('blog_detail', args=(blog.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(
            response,
            f'<a class="button post__button" href="/blog/{blog.id}/post/">New Post</a>',
            html=True,
        )

    def test_creator_add_post(self):
        """
        If authenticated user is blog creator, he will see button for adding new post
        """
        user = create_user('anon')
        blog = create_blog(user, 'Blog title', 'Blog description')

        self.client.login(username='anon', password='testpassword')
        response = self.client.get(reverse('blog_detail', args=(blog.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            f'<a class="button post__button" href="/blog/{blog.id}/post/">New Post</a>',
            html=True,
        )

    def test_post_count_not_auth(self):
        """
        If we add some posts, count should be updated
        """
        user = create_user('anon')
        blog = create_blog(user, 'Blog title', 'Blog description')

        create_post(blog, user, 'Post title', 'Post content', True)
        create_post(blog, user, 'Second title', 'Second Post content', True)

        response = self.client.get(reverse('blog_detail', args=(blog.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'].post_set.count(), 2)

    def test_post_count_one_auth_one_not_user_not_logged(self):
        """
        If we add private and non-private post and user is not logged,
        user will see only 1 post, but post count is still 2
        """
        user = create_user('anon')
        blog = create_blog(user, 'Blog title', 'Blog description')

        create_post(blog, user, 'Post title', 'Post content', True)
        create_post(blog, user, 'Second title', 'Second Post content', False)

        response = self.client.get(reverse('blog_detail', args=(blog.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'].post_set.count(), 2)


class PostDetailViewTests(TestCase):

    def test_no_comments(self):
        """
        If post has no comments, comment count is 0
        """
        user = create_user('anon')
        blog = create_blog(user, 'Blog title', 'Blog description')
        post = create_post(blog, user, 'Post title', 'Post content', True)

        self.client.login(username='anon', password='testpassword')
        response = self.client.get(reverse('post_detail', args=(post.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'].comments.count(), 0)

    def test_comments_count(self):
        """
        If we add comments to a post, post comments count should be updated
        """
        user = create_user('anon')
        blog = create_blog(user, 'Blog title', 'Blog description')
        post = create_post(blog, user, 'Post title', 'Post content', True)

        create_comment(post, user, 'Comment content')

        self.client.login(username='anon', password='testpassword')
        response = self.client.get(reverse('post_detail', args=(post.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'].comments.count(), 1)


class PostCommentsViewTests(TestCase):

    def test_no_comments(self):
        """
        If there's no comments, an appropriate message is displayed
        """
        user = create_user('anon')
        blog = create_blog(user, 'Blog title', 'Blog description')
        post = create_post(blog, user, 'Post title', 'Post content', True)

        # create_comment(post, user, 'Comment content')

        self.client.login(username='anon', password='testpassword')
        response = self.client.get(reverse('post_comments', args=(post.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, 'There are no comments yet, be first to comment!')

    def test_one_comment(self):
        """
        If there's one comment, we should see it
        """
        user = create_user('anon')
        blog = create_blog(user, 'Blog title', 'Blog description')
        post = create_post(blog, user, 'Post title', 'Post content', True)

        create_comment(post, user, 'Comment content')

        self.client.login(username='anon', password='testpassword')
        response = self.client.get(reverse('post_comments', args=(post.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['object'].comments.all(),
            ['<Comment: Blog title: Post title Comment content>'],
        )
