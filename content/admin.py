from django.contrib import admin
from .models import Video

class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'createt_at', 'description']
    search_fields = ['title', 'description']
    list_filter = ['createt_at']
    ordering = ['-createt_at']

admin.site.register(Video, VideoAdmin)
