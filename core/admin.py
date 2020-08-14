from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from core.models import *


class PlaylistAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']
    readonly_fields = ('date_added', 'date_modified', 'id', 'url')
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'visibility')
        }),
        ('Other Details', {
            'fields': ('date_added', 'date_modified', 'url', 'id'),
        }),
    )


admin.site.register(Playlist, SimpleHistoryAdmin)
