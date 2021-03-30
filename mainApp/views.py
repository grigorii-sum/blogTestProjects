from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

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
    if request.user not in post.readers.all():
        post.readers.add(request.user)
    else:
        post.readers.remove(request.user)

    return redirect('feed')


def create_post_page(request):
    if request.method == 'POST':
        if request.POST.get('title') != '' and request.POST.get('text') != '':
            title = request.POST.get('title')
            text = request.POST.get('text')

            name = 'blog of ' + request.user.username
            blog_id = Blog.objects.get(name=name)

            Post.objects.create(title=title, text=text, blog_id=blog_id)

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


class PostDetailView(DetailView):
    model = Post
    template_name = 'main/post_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog'] = Blog.objects.get(id=context['object'].blog_id.id)
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
    template_name = 'main/blog_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(blog_id=context['object']).order_by('-created_at')
        return context


# function for send message (notification) about creating POST model
@receiver(post_save, sender=Post)
def create_post_notification(sender, instance, **kwargs):
    post_obj = Post.objects.get(title=instance)
    blog_obj = Blog.objects.get(id=post_obj.blog_id.id)
    blog_subscriptions = blog_obj.subscriptions.all()

    recipient_list = []
    for obj in blog_subscriptions:
        recipient_list += [obj.email]

    subject = 'В блоге ' + str(blog_obj.name) + ' добавлен новый пост'
    message = 'В блоге ' + str(blog_obj.name) + ' добавлен новый пост\n\n' \
              + 'TITLE: ' + str(post_obj.title) + '\n' \
              + 'TEXT: ' + str(post_obj.text) + '\n' \
              + 'LINK: ' + 'http://localhost:8000/post/' + str(post_obj.id) + '/'
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=False)


# function for send message (notification) about deleting POST model
@receiver(pre_delete, sender=Post)
def delete_post_notification(sender, instance, **kwargs):
    post_obj = Post.objects.get(title=instance)
    blog_obj = Blog.objects.get(id=post_obj.blog_id.id)
    blog_subscriptions = blog_obj.subscriptions.all()

    recipient_list = []
    for obj in blog_subscriptions:
        recipient_list += [obj.email]

    subject = 'В блоге ' + str(blog_obj.name) + ' удален пост'
    message = 'В блоге ' + str(blog_obj.name) + ' удален пост\n\n' \
              + 'TITLE: ' + str(post_obj.title) + '\n' \
              + 'TEXT: ' + str(post_obj.text)
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=False)
