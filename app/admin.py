from django.contrib import admin
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminBase
from .models import (
    Blog,
    CvContent,
    Content,
    Category,
    Tag,
    Comment,
    Task,
    MainRedirections,
    RedirectBlogs,
    RandomRedirection,
)
from django.db import models
from django.utils.html import format_html


from django.utils.html import format_html
from django.contrib import admin
from adminsortable2.admin import SortableInlineAdminMixin
from .models import Content


class ContentInline(SortableInlineAdminMixin, admin.StackedInline):
    model = Content
    extra = 0  # Show only existing content rows by default
    fields = (
        "collapse_button",
        "order",
        "id",
        "content_type",
        "text_content",
        "image_url",
        "link_url",
    )
    readonly_fields = (
        "drag_handle",
        "collapse_button",
    )  # Make drag handle and collapse button read-only

    def drag_handle(self, obj):
        """
        Adds a drag handle for reordering rows.
        """
        return '<span class="drag-handle" style="cursor: move;">⬍</span>'

    drag_handle.allow_tags = True
    drag_handle.short_description = "Drag"

    def collapse_button(self, obj=None):
        """
        Adds a button to toggle the visibility of the current row's fields
        and displays the content type with a brief preview.
        """
        if obj:
            content_preview = ""
            if obj.content_type == "paragraph":
                content_preview = (
                    obj.text_content[:50] + "..." if obj.text_content else "No content"
                )
            elif obj.content_type == "quote":
                content_preview = (
                    f'"{obj.text_content[:50]}"' if obj.text_content else "No quote"
                )
            elif obj.content_type == "link":
                content_preview = obj.link_url if obj.link_url else "No link"
            elif obj.content_type == "image":
                content_preview = "Image uploaded" if obj.image_url else "No image"
            elif obj.content_type == "heading":
                content_preview = (
                    obj.text_content[:50] if obj.text_content else "No heading"
                )

            # Generate the display with the content type and preview
            return format_html(
                '<div style="margin-bottom: 10px;">'
                "<strong>id {}</strong> "
                "</br>"
                "</br>"
                '<strong>Content </strong> {} for "{}" '
                '<button type="button" class="collapse-row-btn" style="cursor: pointer;" '
                'data-row-id="{}">Toggle</button>'
                "</div>",
                obj.id,
                obj.content_type.capitalize(),
                content_preview,
                obj.id if obj else "new-row",
            )
        return format_html(
            '<button type="button" class="collapse-row-btn" style="cursor: pointer;" '
            'data-row-id="new-row">Toggle</button>'
        )

    collapse_button.short_description = "Collapse"
    collapse_button.allow_tags = True

    def get_queryset(self, request):
        """
        Filters the queryset to show only rows with actual content.
        """
        qs = super().get_queryset(request)
        return qs.filter(
            models.Q(text_content__isnull=False) & ~models.Q(text_content="")
            | models.Q(image_url__isnull=False)
            | models.Q(link_url__isnull=False)
        )

    class Media:
        js = ("js/admin_inline_collapse.js",)  # Link to the custom JavaScript file
        css = {
            "all": ("css/admin_inline_collapse.css",),  # Optional: Add custom CSS
        }


class BlogAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ("title", "author", "trend", "created_at")
    search_fields = ("title", "author")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ContentInline]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "blog", "created_at")
    search_fields = ("name", "email", "content")
    list_filter = ("blog", "created_at")


admin.site.register(Blog, BlogAdmin)
admin.site.register(Content)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Task)
admin.site.register(MainRedirections)
admin.site.register(RedirectBlogs)
admin.site.register(RandomRedirection)
admin.site.register(CvContent)
