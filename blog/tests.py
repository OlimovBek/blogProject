from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Post


# Create your tests here.
class BlogTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='user1',
            email='user1@gmail.com',
            password='user1'
        )
        self.post = Post.objects.create(
            title='User 1',
            body='User 1 body',
            author=self.user
        )

    def test_string_representation(self):
        post = Post(title='Post theme')
        self.assertEquals(str(post), post.title)

    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'User 1')
        self.assertEqual(f'{self.post.body}', 'User 1 body')
        self.assertEqual(f'{self.post.author}', 'user1')

    def test_post_list_view(self):
        res = self.client.get(reverse('home'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'User 1 body')
        self.assertTemplateUsed(res, 'home.html')

    def test_post_detail_view(self):
        res = self.client.get('/post/1/')
        no_res = self.client.get('/post/2/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(no_res.status_code, 404)
        self.assertContains(res, 'User 1')
        self.assertTemplateUsed(res, 'post_detail.html')
