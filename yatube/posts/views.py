from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group, User, Comment, Follow
from .forms import PostForm, CommentForm
from .pagin import get_page_context
from core.models import CreatedModel
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator


@cache_page(60 * 20, key_prefix="index_page")
def index(request):
    text = "Последние обновления на сайте"
    title = "Главная страница"
    context = {
        "text": text,
        "title": title,
    }
    context.update(get_page_context(request, Post.objects.all()))
    return render(request, "posts/index.html", context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    context = {
        "group": group,
    }
    context.update(get_page_context(
        request, group.posts.select_related("author", "group")))
    return render(request, "posts/group_list.html", context, slug)


def profile(request, username):
    template = "posts/profile.html"
    author = get_object_or_404(User, username=username)
    if request.user.is_authenticated:
        following = Follow.objects.filter(
            user=request.user,
            author=author
        ).exists
    else:
        following = False
    profile = author
    context = {
        "author": author,
        "username": username,
        "following": following,
        "profile": profile,
    }
    context.update(get_page_context(request, author.posts.all()))
    return render(request, template, context)


def post_detail(request, post_id):
    template = "posts/post_detail.html"
    post_list = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    comments = Comment.objects.select_related("post").filter(post_id=post_id)
    context = {
        "post_list": post_list,
        "post_id": post_id,
        "form": form,
        "comments": comments,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    title = "Новый пост"
    if request.method == "POST":
        form = PostForm(
            request.POST,
            files=request.FILES or None,
        )
        if not form.is_valid():
            return render(request, "posts/create_post.html")
        elif form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
        return redirect("posts:profile", request.user.username)
    form = PostForm()
    context = {
        "title": title,
        "form": form,
    }
    return render(request, "posts/create_post.html", context)


@login_required
def post_edit(request, post_id):
    title = "Редактировать пост"
    is_edit = True
    posts = get_object_or_404(
        Post, id=post_id, author=request.user
    )
    form = PostForm(
        request.POST or None,
        instance=posts
    )
    if request.method == "POST":
        form = PostForm(
            request.POST,
            files=request.FILES or None,
            instance=posts
        )
        if form.is_valid():
            form.save()
            return redirect("posts:post_detail", post_id)
    context = {
        "title": title,
        "is_edit": is_edit,
        "posts": posts,
        "form": form,
        "post_id": post_id,
    }
    return render(request, "posts/create_post.html", context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(
        Post, pk=post_id
    )
    form = CommentForm(request.POST or None)
    template = "posts:post_detail"
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect(template, post_id=post_id)


@login_required
def follow_index(request):
    text = "Мои подписки"
    follow_list = Post.objects.filter(author__following__user=request.user)
    paginator = Paginator(follow_list, 20)
    page_namber = request.GET.get('page_obj')
    page_obj = paginator.get_page(page_namber)
    context = {
        "text": text,
        "page_obj": page_obj,
    }
    return render(request, "posts/follow.html", context)


@login_required
def profile_follow(request, username):
    user = request.user
    author = User.objects.get(username=username)
    is_follower = Follow.objects.filter(user=user, author=author)
    if user != author and not is_follower.exists():
        Follow.objects.create(user=user, author=author)
    return redirect("posts:profile", username=username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    is_follower = Follow.objects.filter(user=request.user, author=author)
    if is_follower.exists():
        is_follower.delete()
    return redirect("posts:index_list")
