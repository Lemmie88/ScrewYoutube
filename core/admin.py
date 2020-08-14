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
        ('Other Details', {
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
        ('Other Details', {
            'fields': BASE_READONLY_FIELDS,
        }),
    )


admin.site.register(Tag, SimpleHistoryAdmin)
