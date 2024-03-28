from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Comment, Location, Post


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('is_published', 'created_at')
    list_display = ('name', 'is_published', 'created_at')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('title', 'description', 'slug')
    list_filter = ('is_published', 'created_at')
    list_display = ('title', 'description', 'is_published', 'created_at')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ('title', 'text', 'author')
    list_filter = ('pub_date', 'author', 'category', 'location',
                   'is_published', 'created_at')
    list_display = ('title', 'display_image', 'author', 'category',
                    'is_published', 'pub_date', 'created_at')

    def display_image(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" width="80" height="60">'
            )
        return 'No Image'

    display_image.short_description = 'Image'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    search_fields = ('text', 'author', 'post', 'created_at')
    list_filter = ('text', 'author', 'post', 'created_at')
    list_display = ('text', 'author', 'post', 'created_at')
