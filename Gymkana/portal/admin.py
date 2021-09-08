from django.contrib import admin

from .models import New, Event

class adminNews(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title']}),
        (None, {'fields': ['subtitle']}),
        (None, {'fields': ['body']}),
        (None, {'fields': ['image']}),
        ('Publish Date', {'fields': ['publish_date']}),
    ]

    list_display = ('title', 'subtitle', 'publish_date')

class adminEvents(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title']}),
        (None, {'fields': ['subtitle']}),
        (None, {'fields': ['body']}),
        ('Start Date', {'fields': ['start_date']}),
        ('End Date', {'fields': ['end_date']}),
    ]

    list_display = ('title', 'subtitle', 'start_date', 'end_date')


admin.site.register(New, adminNews)
admin.site.register(Event, adminEvents)