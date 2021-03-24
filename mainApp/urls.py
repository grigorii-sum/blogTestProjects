from django.urls import path

from .views import login_page, logout_user, BlogListView, PostListView, create_post_page, BlogDetailView, change_post_mark, change_blog_subscription

urlpatterns = [
    # LOG IN and LOG OUT
    path('', login_page, name='login'),
    path('logout/', logout_user, name='logout'),

    # work with POST model
    path('feed/', PostListView.as_view(), name="feed"),
    path('post/create/', create_post_page, name="create-post"),
    path('change_post_mark/<int:id>/', change_post_mark, name='change-mark'),

    # work with BLOG model
    path('blog/all/', BlogListView.as_view(), name="blogs"),
    path('blog/<pk>/', BlogDetailView.as_view(), name='blog-detail'),
    path('change_blog_subscription/<int:id>/', change_blog_subscription, name='change-subscription'),
]
