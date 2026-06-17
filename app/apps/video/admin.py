from django.contrib import admin

from .models import Video


class VideoAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "created_at",
        "title",
        "description",
        "thumbnail_url",
        "category",
    ]
    list_filter = ["created_at"]
    search_fields = ["title", "description"]
    ordering = ["-created_at", "category"]


admin.site.register(Video, VideoAdmin)
