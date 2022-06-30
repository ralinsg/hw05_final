from django import forms
from .models import Post, Comment, Follow


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        labels = {"text": "Текст поста", "group": "Группа"}
        help_texts = {
            "text": "Текст нового поста",
            "group": "Группа, к которой будет относиться пост"
        }
        fields = ("text", "group", "image")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        labels = {
            "text": "Текст комментария",
        }
        help_texts = {
            "text": "Оставьте здесь комментарий",
        }
        fields = ["text"]


class FollowForm(forms.ModelForm):
    class Meta:
        model = Follow
        labels = {
            "user": "Подписка на:",
            "author": "Автор записи",
        }
        fields = ["user"]
