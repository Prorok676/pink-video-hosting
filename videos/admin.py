from django.contrib import admin
from .models import Video, VideoLike, Comment, UserRole


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'is_blocked']
    list_filter = ['is_blocked', 'created_at']
    search_fields = ['title', 'author__username']
    actions = ['block_videos', 'unblock_videos']

    def block_videos(self, request, queryset):
        queryset.update(is_blocked=True)

    block_videos.short_description = "Заблокировать выбранные видео"

    def unblock_videos(self, request, queryset):
        queryset.update(is_blocked=False)

    unblock_videos.short_description = "Разблокировать выбранные видео"


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_admin']
    list_filter = ['is_admin']


admin.site.register(VideoLike)
admin.site.register(Comment)