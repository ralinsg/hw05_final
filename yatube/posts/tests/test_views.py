from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, Client, override_settings
from ..models import Group, Post, Comment, Follow
from ..forms import CommentForm, FollowForm
from django.urls import reverse
from django import forms
import shutil
import tempfile
from django.core.cache import cache
from ..pagin import get_page_context

User = get_user_model()

NUMBER_FIRST_PAGE = 10
NUMBER_SECOND_PAGE = 3
NUMBER_CONTEXT_PAGE = 0
settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=settings.MEDIA_ROOT)
class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
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
        cls.user = User.objects.create_user(username="User1")
        cls.post = Post.objects.create(
            author=cls.user,
            text="Тестовая запись 1",
            image=uploaded,
            group=Group.objects.create(
                title="Тестовая группа",
                slug="test-slug",
                description="Тестовое описание"),
        )
        cls.comment = Comment.objects.create(
            post=cls.post,
            author=cls.user,
            text="Тестовый комментарий 1"
        )
        cls.form = CommentForm()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT)
        super().tearDownClass()

    def setUp(self):
        cache.clear()
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        templates_pages_names = {
            "posts/index.html": reverse("posts:index_list"),
            "posts/group_list.html": reverse(
                "posts:group_list", kwargs={"slug": "test-slug"}
            ),
            "posts/profile.html": reverse(
                "posts:profile", kwargs={"username": self.user}
            ),
            "posts/post_detail.html": reverse(
                "posts:post_detail", kwargs={"post_id": self.post.pk}
            ),
            "posts/create_post.html": reverse(
                "posts:post_edit", kwargs={"post_id": self.post.pk}
            ),
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_context_in_index(self):
        response = self.authorized_client.get(reverse("posts:index_list"))
        first_object = response.context["page_obj"][NUMBER_CONTEXT_PAGE]
        self.assertEqual(first_object.image, "posts/small.gif")
        self.assertEqual(first_object.text, self.post.text)
        self.assertEqual(first_object.group, self.post.group)

    def test_context_in_group_posts(self):
        response = self.authorized_client.get(
            reverse(
                "posts:group_list", kwargs={"slug": "test-slug"}
            )
        )
        first_object = response.context["group"]
        self.assertEqual(Post.objects.first().image, "posts/small.gif")
        self.assertEqual(first_object.title, self.post.group.title)
        self.assertEqual(first_object.slug, self.post.group.slug)

    def test_context_in_profile(self):
        response = self.authorized_client.get(
            reverse(
                "posts:profile", kwargs={"username": self.user}
            )
        )
        first_object = response.context["page_obj"][0]
        self.assertEqual(first_object.image, "posts/small.gif")
        self.assertEqual(first_object.author, self.post.author)
        self.assertEqual(first_object.text, self.post.text)

    def test_context_in_post_detail(self):
        response = self.authorized_client.get(
            reverse(
                "posts:post_detail", kwargs={"post_id": self.post.pk}
            )
        )
        first_object = response.context["post_list"]
        self.assertEqual(first_object.image, "posts/small.gif")
        self.assertEqual(first_object.author, self.user)
        self.assertEqual(first_object.text, self.post.text)
        self.assertEqual(first_object.group.title, self.post.group.title)

    def test_context_in_post_create(self):
        response = self.authorized_client.get(reverse("posts:post_create"))
        form_fields = {
            "group": forms.fields.ChoiceField,
            "text": forms.fields.CharField,
            "image": forms.fields.ImageField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_fields = response.context["form"].fields[value]
                self.assertIsInstance(form_fields, expected)

    def test_context_in_post_edit(self):
        response = self.authorized_client.get(
            reverse(
                "posts:post_edit", kwargs={"post_id": self.post.pk}
            )
        )
        form_fields = {
            "group": forms.fields.ChoiceField,
            "text": forms.fields.CharField,
            "image": forms.fields.ImageField,
        }
        is_edit = True
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_fields = response.context["form"].fields[value]
                self.assertIsInstance(form_fields, expected)
        self.assertEqual(response.context["is_edit"], is_edit)

    def test_correct_show_post(self):
        templates_pages_names = {
            "posts/index.html": reverse("posts:index_list"),
            "posts/group_list.html": reverse(
                "posts:group_list", kwargs={"slug": "test-slug"}
            ),
            "posts/profile.html": reverse(
                "posts:profile", kwargs={"username": self.user}
            ),
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_comments_user(self):
        count_comment = Comment.objects.count()
        form_comment = {
            "text": "Тестовый комментарий 1"
        }
        response = self.authorized_client.post(
            reverse(
                "posts:add_comment", kwargs={"post_id": self.post.pk}
            ),
            data=form_comment,
            follow=True,
        )
        self.assertEqual(Comment.objects.count(), count_comment + 1)
        self.assertContains(response, form_comment["text"])


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="User2")
        cls.group = Group.objects.create(
            title="Тестовая группа",
            slug="test-slug",
            description="Тестовое описание"
        )
        cls.posts = []
        for i in range(13):
            cls.posts.append(Post(
                author=cls.user,
                text=f"Тестовая запись {i}"
            )
            )
        Post.objects.bulk_create(cls.posts)

    def setUp(self):
        cache.clear()
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_first_page_contains_ten_records(self):
        response = self.client.get(reverse("posts:index_list"))
        self.assertEqual(len(response.context["page_obj"]), NUMBER_FIRST_PAGE)

    def test_second_page_contains_three_records(self):
        response = self.client.get(reverse("posts:index_list") + "?page=2")
        self.assertEqual(len(response.context["page_obj"]), NUMBER_SECOND_PAGE)

    def test_page_obj(self):
        templates_page_names = {
            "posts/index.html": reverse("posts:index_list"),
            "posts/group_list.html": reverse(
                "posts:group_list", kwargs={"slug": "test-slug"}
            ),
            "posts/profile.html": reverse(
                "posts:profile", kwargs={"username": self.user}
            ),
        }
        for template, reverse_name in templates_page_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)


class CacheTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="User1")
        cls.post = Post.objects.create(
            author=cls.user,
            text="Тестовая запись 1",)

    def setUp(self):
        cache.clear()
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_cache_index(self):
        first_object = self.authorized_client.get(reverse("posts:index_list"))
        post = Post.objects.get(pk=1)
        post.text = "Тестовый текст поста"
        post.save()
        second_object = self.authorized_client.get(reverse("posts:index_list"))
        self.assertEqual(first_object.content, second_object.content)
        cache.clear()
        third_object = self.authorized_client.get(reverse("posts:index_list"))
        self.assertNotEqual(first_object.content, third_object.content)


class FollowTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.follower = User.objects.create_user(username="User1")
        cls.following = User.objects.create_user(username="User2")
        cls.user_follower = User.objects.create_user(username="User3")
        cls.post = Post.objects.create(
            author=cls.following,
            text="Тестовая запись для подписки",)

    def setUp(self):
        cache.clear()
        self.guest_client = Client()
        self.authorized_follower = Client()
        self.authorized_user_follower = Client()
        self.authorized_following = Client()
        self.authorized_follower.force_login(self.follower)
        self.authorized_user_follower.force_login(self.user_follower)
        self.authorized_following.force_login(self.following)

    def test_post_follow(self):
        self.authorized_follower.get(
            reverse(
                "posts:profile_follow", kwargs={"username": self.following})
        )
        self.assertEqual(Follow.objects.all().count(), 1)

    def test_post_unfollow(self):
        self.authorized_follower.get(
            reverse(
                "posts:profile_follow", kwargs={"username": self.following.username})
        )
        self.authorized_follower.get(
            reverse(
                "posts:profile_unfollow", kwargs={"username": self.following.username})
        )
        self.assertEqual(Follow.objects.all().count(), 0)

    def test_shows_subscriptions(self):
        Follow.objects.create(
            user=self.follower,
            author=self.following
        )
        response = self.authorized_follower.get(reverse("posts:follow_index"))
        first_object = response.context["page_obj"][0].text
        self.assertEqual(first_object, self.post.text)
        response = self.authorized_user_follower.get(
            reverse(
                "posts:follow_index"
            )
        )
        self.assertNotContains(response, self.post.text)

    def test_subscribe_to_yourself(self):
        self.authorized_user_follower.get(
            reverse(
                "posts:profile_follow", kwargs={"username": self.user_follower})
        )
        self.assertEqual(Follow.objects.all().count(), 0)
