from django.shortcuts import render, get_object_or_404
from blog.models import Post
from django.utils import timezone
# Create your views here.

def blog_view(request):
    # posts = Post.objects.all()
    posts = Post.objects.filter(published_date__lte=timezone.now(), status=1).order_by('published_date')
    context = {'posts':posts}
    return render(request, 'blog/blog-home.html', context)


def blog_single(request, pid):
    post = get_object_or_404(Post, id=pid, status=1, published_date__lte=timezone.now())
    post.counted_views += 1
    post.save()

    # posts = list(Post.objects.filter(published_date__lte=timezone.now(), status=1).order_by('published_date'))
    # current_index = posts.index(post)
    # prev_post = posts[current_index - 1] if current_index > 0 else None
    # next_post = posts[current_index + 1] if current_index < len(posts) - 1 else None

    next_post = Post.objects.filter(published_date__gt=post.published_date, status=1).order_by('published_date').first()
    prev_post = Post.objects.filter(published_date__lt=post.published_date, status=1).order_by('-published_date').first()

    context = {
        'post': post,
        'prev_post': prev_post,
        'next_post': next_post,
    }
    return render(request, 'blog/blog-single.html', context)

