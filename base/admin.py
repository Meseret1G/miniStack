from django.contrib import admin

from .models import Post,Title,Message
admin.site.register(Post)
admin.site.register(Title)
admin.site.register(Message)
