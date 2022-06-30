from django.contrib.auth import get_user_model
from django.test import TestCase
from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="auth")
        cls.group = Group.objects.create(
            title="Тестовая группа",
            slug="Тестовый слаг",
            description="Тестовое описание",
        )
        cls.post = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text="Тестовый пост",
        )

    def test_models_have_correct_object_names(self):
        """Тестирование отображения значения  _str_"""
        self.post = PostModelTest.post
        self.group = PostModelTest.group
        field_str_test = {
            self.post: self.post.text[:15],
            self.group: self.group.title,
        }
        for model, expected_values in field_str_test.items():
            with self.subTest(model=model):
                self.assertEqual(expected_values, str(model))

    def test_verbose_name(self):
        """verbose_name поля совпадает с ожидаемым."""
        post = PostModelTest.post
        group = PostModelTest.group
        field_verboses_post = {
            "text": "Текст",
            "pub_date": "Дата публикации",
            "author": "Автор",
            "group": "Группа"
        }
        field_verboses_group = {
            "title": "Название группы",
            "slug": "Уникальный адресс группы",
            "description": "Описание сообщества:"
        }
        for value, expected in field_verboses_post.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).verbose_name, expected
                )
        for value, expected in field_verboses_group.items():
            with self.subTest(value=value):
                self.assertEqual(
                    group._meta.get_field(value).verbose_name, expected
                )

    def test_help_text(self):
        """help_text поля совпадает с ожидаемым."""
        post = PostModelTest.post
        group = PostModelTest.group
        field_help_post = {
            "text": "Текст нового поста",
            "group": "Группа, к которой будет относиться пост",
        }
        field_help_group = {
            "title": "максимум 200 символов",
            "slug": "максимум 100 символов",
        }
        for value, expected in field_help_post.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).help_text, expected
                )
        for value, expected in field_help_group.items():
            with self.subTest(value=value):
                self.assertEqual(
                    group._meta.get_field(value).help_text, expected
                )
