from django.contrib import admin
from .models import Song

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('name', 'artist', 'album_cover')  # 원하는 필드로 수정
