# app/admin.py
from django.contrib import admin
from .models import (Blog, Content,
                     Comment, Tag, Category,
                     RandomRedirection ,
                     RedirectBlogs ,
                     MainRedirections,
                     Task,
                     User,
                     )
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at', 'trend')
    prepopulated_fields = {'slug': ('title',)}
    fields = ('title', 'content', 'slug', 'trend', 'image')  # Include RichTextField

admin.site.register(Content)
admin.site.register(Blog)
admin.site.register(Tag)
admin.site.register(RandomRedirection)
admin.site.register(RedirectBlogs)
admin.site.register(MainRedirections)
admin.site.register(Task)
admin.site.register(User)
