from django.urls import path
from blog.views import *

app_name = 'blog'

urlpatterns = [
    path('', blog_view, name='index'),
    path('<int:pid>', blog_single, name='single'),
    # path('post/<int:post_id>/', blog_single, name='blog_single'),
    # path('post-<int:pid>', test, name='test')
]
