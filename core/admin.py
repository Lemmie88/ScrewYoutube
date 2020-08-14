from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from core.models import *

BASE_FIELDS = ('name', 'description', 'visibility')
BASE_READONLY_FIELDS = ('date_added', 'date_modified', 'url', 'id')


class PlaylistAdmin(admin.ModelAdmin):
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


admin.site.register(Playlist, SimpleHistoryAdmin)


class TagAdmin(admin.ModelAdmin):
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


admin.site.register(Tag, SimpleHistoryAdmin)


class SeriesAdmin(admin.ModelAdmin):
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


admin.site.register(Series, SimpleHistoryAdmin)


class VideoSeries(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']
    readonly_fields = BASE_READONLY_FIELDS
    fieldsets = (
        (None, {
            'fields': BASE_FIELDS,
        }),
        ('Other Details', {
            'fields': ('link', 'series', 'playlist', 'tag'),
        }),
        ('Readonly Details', {
            'fields': BASE_READONLY_FIELDS,
        }),
    )


admin.site.register(Video, SimpleHistoryAdmin)
