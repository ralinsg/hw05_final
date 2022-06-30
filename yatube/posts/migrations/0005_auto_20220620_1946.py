# Generated by Django 2.2.16 on 2022-06-20 16:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0004_auto_20220619_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='slug',
            field=models.SlugField(help_text='максимум 100 символов', unique=True, verbose_name='Уникальный адресс группы'),
        ),
        migrations.AlterField(
            model_name='group',
            name='title',
            field=models.CharField(help_text='максимум 200 символов', max_length=200, verbose_name='Название группы'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(help_text='максимум 400 символов', max_length=400, verbose_name='Текст комментария')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Ссылка на автора поста')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='posts.Post', verbose_name='Ссылка на пост')),
            ],
        ),
    ]
