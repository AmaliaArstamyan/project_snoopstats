from django.contrib import admin
from django.contrib.auth.models import User
from .models import Post, WebsiteInfo

User.objects.all()

admin.site.register(Post)
admin.site.register(WebsiteInfo)

