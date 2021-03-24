from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from .models import Blog, Post


# LOG IN and LOG OUT
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('feed')

    return render(request, 'main/login_page.html')


def logout_user(request):
    logout(request)
    return redirect('login')


# work with POST model
def change_post_mark(request, id):
    post = Post.objects.get(id=id)
    # post.readers.add(request.user)
    if request.user not in post.readers.all():
        post.readers.add(request.user)
    else:
        post.readers.remove(request.user)

    return redirect('feed')


def create_post_page(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get('text')

        name = 'blog of ' + request.user.username
        blog_id = Blog.objects.get(name=name)

        post = Post.objects.create(title=title, text=text, blog_id=blog_id)
        post.save()

        return redirect('feed')

    return render(request, 'main/create_post_page.html')


class PostListView(ListView):
    model = Post
    queryset = Post.objects.all()
    template_name = 'main/list_of_new_posts_page.html'

    def get_auth_user_model(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_blogs = Blog.objects.all()
        all_posts = Post.objects.order_by('-created_at')
        auth_user = self.get_auth_user_model()

        personal_blogs = []
        for obj in all_blogs:
            if auth_user in obj.subscriptions.all():
                personal_blogs += [obj]

        personal_posts = []
        for obj in all_posts:
            if obj.blog_id in personal_blogs:
                personal_posts += [obj]

        context['posts'] = personal_posts
        return context


# work with BLOG model
def change_blog_subscription(request, id):
    blog = Blog.objects.get(id=id)
    if request.user not in blog.subscriptions.all():
        blog.subscriptions.add(request.user)
    else:
        blog.subscriptions.remove(request.user)

    return redirect('blogs')


class BlogListView(ListView):
    model = Blog
    queryset = Blog.objects.order_by('name')
    template_name = 'main/list_of_blogs_page.html'


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'main/blog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(blog_id=context['object'])
        return context

