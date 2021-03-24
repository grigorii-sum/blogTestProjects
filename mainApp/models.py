from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.utils import timezone
from django.dispatch import receiver
from django.contrib.auth.models import User


class Blog(models.Model):
    name = models.CharField(max_length=100)
    subscriptions = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    def __str__(self):
        return self.name

    @receiver(post_save, sender=User)
    def create_user_blog(sender, instance, created, **kwargs):
        if created:
            Blog.objects.create(name='blog of ' + str(instance))


class Post(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    blog_id = models.ForeignKey(Blog, on_delete=models.CASCADE, null=False)
    readers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    def __str__(self):
        return self.title
