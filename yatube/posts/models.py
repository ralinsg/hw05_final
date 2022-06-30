from django.db import models
from core.models import CreatedModel
from django.contrib.auth import get_user_model


User = get_user_model()


class Group(CreatedModel):
    title = models.CharField(
        max_length=200,
        verbose_name="Название группы",
        help_text="максимум 200 символов"
    )
    slug = models.SlugField(
        unique=True,
        verbose_name="Уникальный адресс группы",
        help_text="максимум 100 символов"
    )
    description = models.TextField(
        verbose_name="Описание сообщества:"
    )

    def __str__(self) -> str:
        return self.title


class Post(CreatedModel):
    text = models.TextField(
        verbose_name="Текст",
        help_text="Текст нового поста"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="posts",
        verbose_name="Автор"
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        related_name="posts",
        on_delete=models.SET_NULL,
        verbose_name="Группа",
        help_text="Группа, к которой будет относиться пост"
    )
    image = models.ImageField(
        "Картинка",
        upload_to="posts/",
        blank=True
    )

    def __str__(self) -> str:
        return self.text

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ["-pub_date"]


class Comment(CreatedModel):
    post = models.ForeignKey(
        Post,
        related_name="comments",
        verbose_name="Ссылка на пост",
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        related_name="comments",
        verbose_name="Ссылка на автора поста",
        on_delete=models.CASCADE
    )
    text = models.TextField(
        verbose_name="Текст комментария",
        help_text="максимум 400 символов"
    )

    def __str__(self) -> str:
        return self.text


class Follow(CreatedModel):
    user = models.ForeignKey(
        User,
        related_name="follower",
        verbose_name="Ссылка на объект, который подписывается",
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        related_name="following",
        verbose_name="Ссылка на объект, на которого подписываются",
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("user", "author")
