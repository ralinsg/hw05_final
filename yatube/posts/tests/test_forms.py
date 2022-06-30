import shutil
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from ..models import Group, Post
from django.urls import reverse
from http import HTTPStatus


User = get_user_model()
settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=settings.MEDIA_ROOT)
class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="User1")
        cls.post = Post.objects.create(
            author=cls.user,
            text="Тестовая запись 1",)
        cls.group = Group.objects.create(
            title="Тестовая группа",
            slug="test-slug",
            description="Тестовое описание")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT)
        super().tearDownClass()

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        post_count = Post.objects.count()
        form_data = {
            "author": self.user,
            "text": "Тестовая запись 1"
        }
        response = self.authorized_client.post(
            reverse("posts:post_create"),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            "posts:profile", kwargs={"username": self.user}
        )
        )
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertTrue(
            Post.objects.filter(
                author=self.user,
                text="Тестовая запись 1",
            ).exists()
        )

    def test_edit_post(self):
        form_data = {
            "author": self.user,
            "text": "Тестовая запись 1",
            "group": self.group.id
        }
        post_edit = Post.objects.get(id=self.group.id)
        self.authorized_client.post(
            reverse("posts:post_edit",
                    kwargs={"post_id": post_edit.id}),
            data=form_data,
            follow=True,
        )
        self.client.get(f"/user1/{post_edit.id}/edit/")
        form_data = {
            "author": self.user,
            "text": "Измененная запись 2",
            "group": self.group.id
        }
        response_edit = self.authorized_client.post(
            reverse(
                "posts:post_edit", kwargs={"post_id": post_edit.id}
            ),
            data=form_data,
            follow=True,
        )
        post_edit = Post.objects.get(id=self.group.id)
        self.assertTrue(
            Post.objects.filter(
                author=self.user,
                text="Измененная запись 2",
                group=self.group.id
            ).exists()
        )
        self.assertEqual(post_edit.text, "Измененная запись 2")
        self.assertEqual(response_edit.status_code, HTTPStatus.OK)

    def test_post_image(self):
        posts_count = Post.objects.count()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name="small.gif",
            content=small_gif,
            content_type="image/gif"
        )
        form_data = {
            "text": "Пост с картинкой",
            "group": self.group.id,
            "image": uploaded
        }
        response = self.authorized_client.post(
            reverse("posts:post_create"),
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertRedirects(response, reverse(
            "posts:profile", kwargs={"username": self.user}
        )
        )
