from django.contrib import admin
from .models import Post, Comment

# register Post in admin GUI site
admin.site.register(Post)
admin.site.register(Comment)