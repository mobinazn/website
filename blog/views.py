from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post, Comment
from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from blog.forms import CommentForm
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
# Create your views here.

def blog_view(request, **kwargs):
    posts = Post.objects.filter(published_date__lte=timezone.now(), status=1).order_by('-published_date')
    if kwargs.get('cat_name') != None:
        posts = posts.filter(category__name=kwargs['cat_name'])
    if kwargs.get('author_username') != None:
        posts = posts.filter(author__username=kwargs['author_username'])
    if kwargs.get('tag_name') != None:
        posts = posts.filter(tags__name__in=[kwargs['tag_name']])
    posts = Paginator(posts, 3)
    try:
        page_number = request.GET.get('page')
        posts = posts.get_page(page_number)
    except PageNotAnInteger:
        posts = posts.get_page(1)
    except EmptyPage:
        posts = posts.get_page(1)

    latest_posts = posts[:3]

    context = {
        'posts':posts,
        'latest_posts': latest_posts
        }
    return render(request, 'blog/blog-home.html', context)


def blog_single(request, pid):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'your comment submitted successfully' )
        else:
            messages.add_message(request, messages.ERROR, 'your comment didn\'t submit' )


    post = get_object_or_404(Post, id=pid, status=1, published_date__lte=timezone.now())
    post.counted_views += 1
    post.save()

    # posts = list(Post.objects.filter(published_date__lte=timezone.now(), status=1).order_by('published_date'))
    # current_index = posts.index(post)
    # prev_post = posts[current_index - 1] if current_index > 0 else None
    # next_post = posts[current_index + 1] if current_index < len(posts) - 1 else None

    next_post = Post.objects.filter(published_date__gt=post.published_date, status=1).order_by('published_date').first()
    prev_post = Post.objects.filter(published_date__lt=post.published_date, status=1).order_by('-published_date').first()

    if not post.login_required:
        comments = Comment.objects.filter(post=post.id, approved=True)
        form = CommentForm()
        context = {
            'post': post,
            'prev_post': prev_post,
            'next_post': next_post,
            'comments': comments,
            'form': form
        }
        return render(request, 'blog/blog-single.html', context)
    else:
        return HttpResponseRedirect(reverse('accounts:login'))


# def test(request):
#     return render(request, 'test.html')


def blog_category(request,cat_name):
    posts = Post.objects.filter(status=1)
    posts = posts.filter(category__name=cat_name)
    context = {'posts':posts}
    return render(request, 'blog/blog-home.html', context)


def blog_search(request):
    posts = Post.objects.filter(published_date__lte=timezone.now(), status=1).order_by('published_date')
    if request.method == 'GET':
        if s := request.GET.get('s'):
            posts = posts.filter(content__contains=s)
    context = {'posts':posts}
    return render(request, 'blog/blog-home.html', context)
