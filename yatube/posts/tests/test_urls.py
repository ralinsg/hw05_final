from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from ..models import Group, Post
from http import HTTPStatus

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="User1")
        cls.group = Group.objects.create(
            title="Тестовая группа",
            slug="test-slug",
            description="Тестовое описание",
        )
        cls.post = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text="Тестовый пост",
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.guest_url = {
            "/": "posts/index.html",
            "/group/test-slug/": "posts/group_list.html",
            "/profile/User1/": "posts/profile.html",
            f"/posts/{PostURLTests.post.id}/": "posts/post_detail.html",
        }
        self.authorized_user_url = {
            "/create/": "posts/create_post.html",
            f"/posts/{PostURLTests.post.id}/edit/": "posts/create_post.html",
        }

    def test_guest_url_code_200(self):
        for address, template in self.guest_url.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_uthorized_user_url_code_200(self):
        for address, template in self.authorized_user_url.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_response_404(self):
        response = self.guest_client.get("/gamepost/")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
