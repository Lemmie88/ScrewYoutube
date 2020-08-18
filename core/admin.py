from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from core.models import *

BASE_FIELDS = ('name', 'description', 'visibility')
BASE_READONLY_FIELDS = ('date_added', 'date_modified', 'url', 'id')


class PlaylistAdmin(SimpleHistoryAdmin):
    ordering = ['name']
    search_fields = ['name']
    readonly_fields = BASE_READONLY_FIELDS
    fieldsets = (
        (None, {
            'fields': BASE_FIELDS,
        }),
        ('Readonly Details', {
            'fields': BASE_READONLY_FIELDS,
        }),
    )


admin.site.register(Playlist, PlaylistAdmin)


class TagAdmin(SimpleHistoryAdmin):
    ordering = ['name']
    search_fields = ['name']
    readonly_fields = BASE_READONLY_FIELDS
    fieldsets = (
        (None, {
            'fields': BASE_FIELDS,
        }),
        ('Readonly Details', {
            'fields': BASE_READONLY_FIELDS,
        }),
    )


admin.site.register(Tag, TagAdmin)


class SeriesAdmin(SimpleHistoryAdmin):
    ordering = ['name']
    search_fields = ['name']
    readonly_fields = BASE_READONLY_FIELDS
    fieldsets = (
        (None, {
            'fields': BASE_FIELDS,
        }),
        ('Readonly Details', {
            'fields': BASE_READONLY_FIELDS,
        }),
    )


admin.site.register(Series, SeriesAdmin)


class ThumbnailAdmin(SimpleHistoryAdmin):
    ordering = ['video', 'position']
    search_fields = ['video__name']
    readonly_fields = ('id',)
    fieldsets = (
        (None, {
            'fields': ('video', 'position', 'public_url',),
        }),
        ('Readonly Details', {
            'fields': ('id',),
        }),
    )


admin.site.register(Thumbnail, ThumbnailAdmin)


class VideoAdmin(SimpleHistoryAdmin):
    ordering = ['name']
    search_fields = ['name']
    readonly_fields = BASE_READONLY_FIELDS
    fieldsets = (
        (None, {
            'fields': BASE_FIELDS,
        }),
        ('Other Details', {
            'fields': ('video', 'public_url', 'duration', 'status', 'link', 'series', 'playlist', 'tag'),
        }),
        ('Readonly Details', {
            'fields': BASE_READONLY_FIELDS,
        }),
    )


admin.site.register(Video, VideoAdmin)
