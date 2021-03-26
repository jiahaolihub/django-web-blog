from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE) # Once user is deleted, user's posts also will be deleted
    likes = models.ManyToManyField(User, related_name="blog_posts")

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    # let django knows how to return/reverse full absoulte url
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
        

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)

