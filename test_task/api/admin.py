from django.contrib import admin

from .models import Page, Video, Audio, Text


class VideoInline(admin.TabularInline):
    model = Video
    extra = 1


class AudioInline(admin.TabularInline):
    model = Audio
    extra = 1


class TextInline(admin.TabularInline):
    model = Text
    extra = 1


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    inlines = [VideoInline, AudioInline, TextInline]
    search_fields = ['title']


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_display = ['title', 'text', 'page']
    list_filter = ['page']
    search_fields = ['title']


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'video_url', 'subtitles_url', 'page']
    list_filter = ['page']
    search_fields = ['title']


@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    list_display = ['title', 'bitrate', 'page']
    list_filter = ['page']
    search_fields = ['title']
